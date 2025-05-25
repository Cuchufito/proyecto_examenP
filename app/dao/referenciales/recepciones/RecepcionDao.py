# app/dao/recepciones/RecepcionDao.py
from flask import current_app as app
from app.conexion.Conexion import Conexion

class RecepcionDao:
    """DAO para gestionar las recepciones de vehículo"""

    def get_all(self):
        sql = """
        SELECT recepcion_id,
               fecha_recepcion,
               motivo_ingreso,
               kilometraje,
               nivel_combustible,
               porcentaje_combustible,
               observaciones,
               estado,
               vehiculo_id
        FROM recepciones
        ORDER BY recepcion_id
        """
        conn = Conexion().getConexion()
        cur = conn.cursor()
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            return [{
                'recepcion_id': r[0],
                'fecha_recepcion': r[1],
                'motivo_ingreso': r[2],
                'kilometraje': r[3],
                'nivel_combustible': r[4],
                'porcentaje_combustible': r[5],
                'observaciones': r[6],
                'estado': r[7],
                'vehiculo_id': r[8]
            } for r in rows]
        except Exception as e:
            app.logger.error(f"Error al obtener recepciones: {e}")
            return []
        finally:
            cur.close()
            conn.close()

    def get_by_id(self, recepcion_id):
        sql = """
        SELECT recepcion_id,
               fecha_recepcion,
               motivo_ingreso,
               kilometraje,
               nivel_combustible,
               porcentaje_combustible,
               observaciones,
               estado,
               vehiculo_id
        FROM recepciones
        WHERE recepcion_id = %s
        """
        conn = Conexion().getConexion()
        cur = conn.cursor()
        try:
            cur.execute(sql, (recepcion_id,))
            r = cur.fetchone()
            if not r:
                return None
            return {
                'recepcion_id': r[0],
                'fecha_recepcion': r[1],
                'motivo_ingreso': r[2],
                'kilometraje': r[3],
                'nivel_combustible': r[4],
                'porcentaje_combustible': r[5],
                'observaciones': r[6],
                'estado': r[7],
                'vehiculo_id': r[8]
            }
        except Exception as e:
            app.logger.error(f"Error al obtener recepción por ID: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    def create(self,
               vehiculo_id,
               motivo_ingreso,
               kilometraje,
               nivel_combustible,
               porcentaje_combustible,
               observaciones,
               estado='pendiente'):
        sql = """
        INSERT INTO recepciones (
            vehiculo_id,
            motivo_ingreso,
            kilometraje,
            nivel_combustible,
            porcentaje_combustible,
            observaciones,
            estado
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING recepcion_id
        """
        conn = Conexion().getConexion()
        cur = conn.cursor()
        try:
            cur.execute(sql, (
                vehiculo_id,
                motivo_ingreso,
                kilometraje,
                nivel_combustible,
                porcentaje_combustible,
                observaciones,
                estado
            ))
            new_id = cur.fetchone()[0]
            conn.commit()
            return new_id
        except Exception as e:
            app.logger.error(f"Error al guardar recepción: {e}")
            conn.rollback()
            return None
        finally:
            cur.close()
            conn.close()

    def update(self,
               recepcion_id,
               vehiculo_id,
               motivo_ingreso,
               kilometraje,
               nivel_combustible,
               porcentaje_combustible,
               observaciones,
               estado):
        sql = """
        UPDATE recepciones
        SET vehiculo_id = %s,
            motivo_ingreso = %s,
            kilometraje = %s,
            nivel_combustible = %s,
            porcentaje_combustible = %s,
            observaciones = %s,
            estado = %s
        WHERE recepcion_id = %s
        """
        conn = Conexion().getConexion()
        cur = conn.cursor()
        try:
            cur.execute(sql, (
                vehiculo_id,
                motivo_ingreso,
                kilometraje,
                nivel_combustible,
                porcentaje_combustible,
                observaciones,
                estado,
                recepcion_id
            ))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar recepción: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()

    def delete(self, recepcion_id):
        sql = "DELETE FROM recepciones WHERE recepcion_id = %s"
        conn = Conexion().getConexion()
        cur = conn.cursor()
        try:
            cur.execute(sql, (recepcion_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar recepción: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
