import secrets
import re
import hmac
import unicodedata

class RedactionError(Exception):
    pass

def generate_api_key():
    return f"sk-numnum-{secrets.token_urlsafe(32)}"

def verify_api_key(provided_key: str, actual_key: str) -> bool:
    if not provided_key or not actual_key:
        return False
    try:
        return hmac.compare_digest(provided_key.encode(), actual_key.encode())
    except Exception:
        return False

def redact_secrets(text: str) -> str:
    if not text:
        return text
    
    try:
        # Normalize text to prevent zero-width character bypasses
        text = unicodedata.normalize("NFKC", text)
        
        patterns = [
            # API Keys & Tokens (Using negative lookbehind to prevent 'risk-' false positives)
            (r'(?<![a-zA-Z0-9])(sk-[a-zA-Z0-9_-]{20,})', '[REDACTED_API_KEY]'),
            (r'(ghp_[a-zA-Z0-9]{36})', '[REDACTED_GITHUB_TOKEN]'),
            (r'(github_pat_[a-zA-Z0-9_]{82})', '[REDACTED_GITHUB_PAT]'),
            (r'(AKIA[0-9A-Z]{16})', '[REDACTED_AWS_KEY]'),
            (r'(?i)(aws_secret_access_key|aws_secret_key)\s*=\s*[A-Za-z0-9/+=]{40}', r'\1=[REDACTED_AWS_SECRET]'),
            (r'(eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)', '[REDACTED_JWT]'),
            
            # Databases
            (r'(?i)(postgres|postgresql|mysql|mongodb|redis):\/\/[^:\s]+:[^@\s]+@', r'\1://[REDACTED_USER]:[REDACTED_PASS]@'),
            
            # Private Keys
            (r'-----BEGIN (RSA|EC|OPENSSH|PRIVATE) PRIVATE KEY-----[\s\S]*?-----END \1 PRIVATE KEY-----', '[REDACTED_PEM_KEY]'),
            
            # Generic Passwords (JSON, YAML, CLI, and Prose)
            (r'(?i)(password|passwd|pwd|secret|token|api_key)(\s*[:=]\s*|--)(?!"\[REDACTED)([^\s"\'\n]+)', r'\1\2"[REDACTED_SECRET]"')
        ]
        
        redacted = text
        for pattern, replacement in patterns:
            redacted = re.sub(pattern, replacement, redacted)
            
        return redacted
    except Exception as e:
        # Fail-Closed: Agar redaction fail ho, toh publish mat hone do
        raise RedactionError(f"Security failure during redaction: {str(e)}")