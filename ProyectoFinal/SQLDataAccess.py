import os
import json
import pandas as pd

class SQLDataAccess:
    # Parámetros de configuración de conexión
    _CLAVES = ('server', 'user', 'password', 'database')

    def __init__(self, server, user, password, database,
                 driver='ODBC Driver 17 for SQL Server',
                 port=1433, backend='auto',
                 trust_server_certificate=True, timeout=30):

        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.driver = driver
        self.port = port
        self.trust_server_certificate = trust_server_certificate
        self.timeout = timeout
        self.backend = self._resolver_backend(backend)
        self._conn = None
        self.consultas = {}   # SQL guardado por nombre (se llena desde el JSON)

    # ---------- Constructores alternativos ----------
    # ------------------------------------------------

    @classmethod
    def desde_config(cls, config):
        faltan = [k for k in cls._CLAVES if k not in config]
        if faltan:
            raise KeyError(f"Faltan claves en la configuración: {faltan}")
        return cls(server=config['server'], user=config['user'],
                   password=config['password'], database=config['database'])

    @classmethod
    def desde_json(cls, ruta='db_config.json', clave='db_config',
                   clave_consultas='consultas'):
        """Carga las credenciales (y las consultas guardadas) desde un JSON. """
        if not os.path.exists(ruta):
            raise FileNotFoundError(
                f"No se encontró '{ruta}'.")
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
        config = data[clave] if clave else data
        obj = cls.desde_config(config)
        if clave_consultas:
            obj.consultas = data.get(clave_consultas, {})
        return obj

    # ---------- Manejo de la conexión ----------
    # -------------------------------------------

    def _resolver_backend(self, backend):
        if backend in ('pyodbc', 'pymssql'):
            return backend
        # auto: preferir pyodbc, si no está usar pymssql
        try:
            import pyodbc  # noqa: F401
            return 'pyodbc'
        except ImportError:
            try:
                import pymssql  # noqa: F401
                return 'pymssql'
            except ImportError:
                raise ImportError(
                    "No existe conector a la base de datos.")

    def _cadena_pyodbc(self):
        partes = [
            f"DRIVER={{{self.driver}}}",
            f"SERVER={self.server},{self.port}",
            f"DATABASE={self.database}",
            f"UID={self.user}",
            f"PWD={self.password}",
            f"Connection Timeout={self.timeout}",
        ]
        if self.trust_server_certificate:
            partes.append("TrustServerCertificate=yes")
        return ";".join(partes) + ";"

    def conectar(self):
        """Abre la conexión """
        if self._conn is not None:
            return self._conn
        if self.backend == 'pyodbc':
            import pyodbc
            self._conn = pyodbc.connect(self._cadena_pyodbc())
        else:
            import pymssql
            self._conn = pymssql.connect(
                server=self.server, user=self.user, password=self.password,
                database=self.database, port=str(self.port), login_timeout=self.timeout)
        return self._conn

    def cerrar(self):
        """Cierra la conexión si está abierta."""
        if self._conn is not None:
            try:
                self._conn.close()
            finally:
                self._conn = None

    def probar_conexion(self, verbose=True):
        """Devuelve True si puede conectar y ejecutar un SELECT trivial."""
        try:
            df = self.consultar("SELECT 1 AS ok")
            ok = int(df.iloc[0, 0]) == 1
            if verbose and ok:
                print(f"Conexión OK -> {self.server}/{self.database} "
                      f"(backend={self.backend})")
            return ok
        except Exception as e:
            if verbose:
                print(f"Falló la conexión: {type(e).__name__}: {e}")
            return False

    # ---------- Lectura de datos ----------
    # --------------------------------------

    def consultar(self, sql, params=None):
        """Ejecuta un SELECT y devuelve un DataFrame con los resultados. """
        import warnings
        conn = self.conectar()
        with warnings.catch_warnings():
            # pandas avisa cuando no se usa SQLAlchemy; la lectura funciona igual.
            warnings.simplefilter('ignore', UserWarning)
            return pd.read_sql(sql, conn, params=params)

    def sql_guardada(self, nombre):
        """Devuelve el texto SQL de una consulta guardada en el JSON.  """
        if nombre not in self.consultas:
            disponibles = ", ".join(self.consultas) or "(ninguna)"
            raise KeyError(
                f"No existe la consulta '{nombre}'. Disponibles: {disponibles}")
        sql = self.consultas[nombre]
        if isinstance(sql, (list, tuple)):
            sql = "\n".join(sql)
        return sql

    def consultar_sql(self, nombre, params=None):
        """Ejecuta una consulta guardada por nombre y devuelve un DataFrame."""
        return self.consultar(self.sql_guardada(nombre), params=params)

    def leer_tabla(self, tabla, columnas=None, where=None, params=None,
                   limite=None, esquema='dbo'):
        """Lee una tabla/vista construyendo el SELECT por ti. """
        cols = ", ".join(columnas) if columnas else "*"
        top = f"TOP {int(limite)} " if limite else ""
        sql = f"SELECT {top}{cols} FROM [{esquema}].[{tabla}]"
        if where:
            sql += f" WHERE {where}"
        return self.consultar(sql, params=params)

    def listar_tablas(self, esquema=None):
        """Devuelve un DataFrame con las tablas y vistas de la base de datos."""
        sql = ("SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE "
               "FROM INFORMATION_SCHEMA.TABLES")
        params = None
        if esquema:
            sql += " WHERE TABLE_SCHEMA = ?"
            params = [esquema]
        sql += " ORDER BY TABLE_SCHEMA, TABLE_NAME"
        return self.consultar(sql, params=params)

    def columnas_de(self, tabla, esquema='dbo'):
        """Devuelve las columnas y tipos de una tabla (útil para mapear el CFG)."""
        sql = ("SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE "
               "FROM INFORMATION_SCHEMA.COLUMNS "
               "WHERE TABLE_NAME = ? AND TABLE_SCHEMA = ? "
               "ORDER BY ORDINAL_POSITION")
        return self.consultar(sql, params=[tabla, esquema])

