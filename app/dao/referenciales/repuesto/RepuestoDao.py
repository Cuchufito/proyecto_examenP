from flask import current_app as app
from app.conexion.Conexion import Conexion

class RepuestoDao:

    def getRepuesto(self):
        repuestoSQL = """
        SELECT id, repuesto, codigo
        FROM repuestos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(repuestoSQL)
            repuestos = cur.fetchall()  # trae datos de la bd

            # Transformar los datos en una lista de diccionarios
            return [{'id': repuesto[0], 'repuesto': repuesto[1], 'codigo': repuesto[2]} for repuesto in repuestos]

        except Exception as e:
            app.logger.error(f"Error al obtener todos los repuestos: {str(e)}")
            return []

        finally:
            cur.close()
            con.close()

    def getRepuestoById(self, id):
        repuestoSQL = """
        SELECT id, repuesto, codigo
        FROM repuestos WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(repuestoSQL, (id,))
            repuestoEncontrado = cur.fetchone()  # Obtener una sola fila
            if repuestoEncontrado:
                return {
                    "id": repuestoEncontrado[0],
                    "repuesto": repuestoEncontrado[1],
                    "codigo": repuestoEncontrado[2]
                }  # Retornar los datos de la repuesto
            else:
                return None  # Retornar None si no se encuentra la repuesto
        except Exception as e:
            app.logger.error(f"Error al obtener repuesto: {str(e)}")
            return None

        finally:
            cur.close()
            con.close()

    def guardarRepuesto(self, repuesto, codigo):
        insertarRepuestoSQL = """
        INSERT INTO repuestos(repuesto, codigo) VALUES(%s, %s) RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(insertarRepuestoSQL, (repuesto, codigo))
            repuesto_id = cur.fetchone()[0]
            con.commit()  # se confirma la inserción
            return repuesto_id

        except Exception as e:
            app.logger.error(f"Error al insertar repuesto: {str(e)}")
            con.rollback()  # retroceder si hubo error
            return False

        finally:
            cur.close()
            con.close()

    def updateRepuesto(self, id, repuesto, codigo):
        updateRepuestoSQL = """
        UPDATE repuestos
        SET repuesto=%s, codigo=%s
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(updateRepuestoSQL, (repuesto, codigo, id,))
            filas_afectadas = cur.rowcount  # Obtener el número de filas afectadas
            con.commit()

            return filas_afectadas > 0  # Retornar True si se actualizó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al actualizar repuesto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()

    def deleteRepuesto(self, id):
        deleteRepuestoSQL = """
        DELETE FROM repuestos
        WHERE id=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(deleteRepuestoSQL, (id,))
            rows_affected = cur.rowcount
            con.commit()

            return rows_affected > 0  # Retornar True si se eliminó al menos una fila

        except Exception as e:
            app.logger.error(f"Error al eliminar repuesto: {str(e)}")
            con.rollback()
            return False

        finally:
            cur.close()
            con.close()
