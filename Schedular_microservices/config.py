
class Config:
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.example.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USER = os.getenv('EMAIL_USER', 'your-email@example.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-email-password')
    EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER', 'recipient@example.com')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    DB_NAME = os.getenv('DB_NAME', 'postgres')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
