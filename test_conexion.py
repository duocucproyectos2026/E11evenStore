from sqlalchemy import create_engine

DATABASE_URL = "oracle+oracledb://system:Ora1234@127.0.0.1:1521/?service_name=freepdb1"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("✅ Conexión a Oracle exitosa")
except Exception as e:
    print("❌ Error al conectar con Oracle:")
    print(e)
