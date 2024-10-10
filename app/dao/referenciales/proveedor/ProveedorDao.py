from flask import current_app as app
from app.conexion.Conexion import Conexion

class ProveedorDao:

    def getProveedores(self):
        proveedorSQL = """
        SELECT id, ruc, razon_social
        FROM proveedores
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(proveedorSQL)
            proveedores = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': proveedor[0], 'ruc': proveedor[1], 'razon_social': proveedor[2]} for proveedor in proveedores]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los proveedores: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getProveedorById(self, id):
        proveedorSQL = """
        SELECT id, ruc, razon_social
        FROM proveedores WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(proveedorSQL, (id,))
            proveedorEncontrado = cur.fetchone()  # Obtener una sola fila
            if proveedorEncontrado:
                return {
                    "id": proveedorEncontrado[0],
                    "ruc": proveedorEncontrado[1],
                    "razon_social": proveedorEncontrado[2]
                }  # Retornar los datos del proveedor
            else:
                return None  # Retornar None si no se encuentra el proveedor
        except Exception as e:
            app.logger.error(f"Error al obtener proveedor: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarProveedor(self, ruc, razon_social):
        insertProveedorSQL = """
        INSERT INTO proveedores(ruc, razon_social) VALUES(%s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertProveedorSQL, (ruc, razon_social))
            proveedor_id = cur.fetchone()[0]
            con.commit()  # se confirma la inserción
            return proveedor_id

        except Exception as e:
            app.logger.error(f"Error al insertar proveedor: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateProveedor(self, id, ruc, razon_social):
        updateProveedorSQL = """
        UPDATE proveedores
        SET ruc=%s, razon_social=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateProveedorSQL, (ruc, razon_social, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar proveedor: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteProveedor(self, id):
        deleteProveedorSQL = """
        DELETE FROM proveedores
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteProveedorSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar proveedor: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
