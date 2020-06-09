import pymysql
from Cosas.Protocolo import Protocolo


class database_model:

    protocolo = None
    conexion = None
    cursor = None

    def __init__(self, pro):

        self.protocolo = pro

    """
        @brief Método que va a crear la aconexión
        @date 07/05/2020
        @author Alexinio
    """
    def crearConexion(self):
        try:
            self.conexion = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                db='tfc'
            )
        except Exception as e:
            print("Excepcion al conectar con la base de datos: ", e)

    """
        @brief Método que va a cerrar la aconexión
        @date 07/05/2020
        @author Alexinio
    """
    def cerrarConexion(self):

        self.conexion.close()

    """
        @brief Método que va a comprobar si el usuario que se está intentando registrar es un alumno o un profesor
        @author Alexinio
        @date 07/05/2020
        @param dni es el dni de la persona
        @param passwd es la constraseña del usuario
    """
    def comprobarLogin(self, dni, passwd):

        registrado = "error"

        if self.comprobarLoginAlumno(dni, passwd):
            registrado = "alumno"

        elif self.comprobarLoginProfesor(dni, passwd):
            registrado = "profesor"

        return registrado

        #print("Lo que hemos conseguido de la base de datos: {}, {}, {}".format(cosa[0], cosa[1], cosa[2]))

    """
        @brief Método que va a comprobar si existe registrada un alumno con el dni y la constraseña pasadsos
        @author Alexinio
        @date 07/05/2020
        @param dni es el dni de la persona
        @param passwd es la constraseña del usuario
    """
    def comprobarLoginAlumno(self, dni, passwd):

        try:
            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "SELECT * FROM estudiante WHERE dni_estudiante='{}' AND passwd_estudiante='{}';".format(dni, passwd)
            print("Query (comprobarLoginAlumno): ", query)

            self.cursor.execute(query)
            cosa = self.cursor.fetchall()

            registrado = False

            for user in cosa:
                #print("DNI estudiante: {}".format(user[0]))
                #print("Nombre estudiante: {}".format(user[1]))
                #print("Apellidos estudiante: {}".format(user[2]))
                registrado = True

            self.cerrarConexion()
        except Exception as e:
            self.cerrarConexion()
            print("Excepcion en comprbarLoginAlumno: ", e)

        return registrado

    """
        @brief Método que va a comprobar si existe registrada un profesor con el dni y la constraseña pasadsos
        @author Alexinio
        @date 07/05/2020
        @param dni, dni del profesor 
        @param passwd es la constraseña del usuario
    """
    def comprobarLoginProfesor(self, dni, passwd):

        try:
            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "SELECT * FROM profesor WHERE dni_prof='{}' AND passwd_prof='{}';".format(dni, passwd)
            print("Query (comprobarLoginProfesor): ", query)

            self.cursor.execute(query)
            cosa = self.cursor.fetchall()

            registrado = False

            for user in cosa:
                #print("DNI profesor: {}".format(user[0]))
                #print("Nombre profesor: {}".format(user[1]))
                #print("Apellidos profesor: {}".format(user[2]))
                registrado = True

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Expcecion en comprobarLoginProfesor: ", e)

        return registrado

    """
        @brief Método que va a obtener la info que está resgistrada en la base de datos correspondiente al dni y la contraseña pasados
        @author Alexinio
        @date 07/05/2020
        @param dni es el dni de la persona
        @param passwd es la constraseña del usuario
    """
    def getInfoAlumno(self, dni, passwd):

        try:
            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "SELECT * FROM estudiante WHERE dni_estudiante='{}' AND passwd_estudiante='{}';".format(dni, passwd)
            print("Query (getInfoAlumno): ", query)

            self.cursor.execute(query)
            cosa = self.cursor.fetchall()

            info = None;

            for user in cosa:
                print("DNI estudiante: {}".format(user[0]))
                print("Passwd estudiante: {}".format(user[1]))
                print("Nombre estudiante: {}".format(user[2]))
                print("Apellidos estudiante: {}".format(user[3]))
                print("Centro estudiante: {}".format(user[4]))

                dni = user[0]
                name = user[1]
                surnames = user[2]

                info = str(dni) + "%" + str(name) + "%" + str(surnames)


                #info = dni + "%" + name + "%" + surnames
                print("Info del alumno que vamos a pillar ahi a tope bro: ", info)

            #print("vamos a revolver los valores que cojemos de la base de datoss")
            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion engetInfoAlumno: ", e)

        return info

    """
        @brief Método que va a obtener la info que está resgistrada en la base de datos correspondiente al dni y la contraseña pasados
        @author Alexinio
        @date 07/05/2020
        @param dni es el dni de la persona
        @param passwd es la constraseña del usuario
    """
    def getInfoProfesor(self, dni, passwd):

        try:

            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "SELECT * FROM profesor WHERE dni_prof='{}' AND passwd_prof='{}';".format(dni, passwd)
            print("Query (getInfoProfesor): ", query)

            self.cursor.execute(query)
            cosa = self.cursor.fetchall()

            info = None

            for user in cosa:
                print("DNI prof: {}".format(user[0]))
                print("passwd prof: {}".format(user[1]))
                print("nombre prof: {}".format(user[2]))
                print("apellidos prof: {}".format(user[3]))
                print("centro prof: {}".format(user[4]))

                info = str(user[0]) + "%" + str(user[4]) + "%" + str(user[2]) + "%" + str(user[3])

                #info = dni + "%" + name + "%" + surnames
                print("Info del profesor que vamos a pillar ahi a tope bro: ", info)

            #print("vamos a revolver los valores que cojemos de la base de datoss")
            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion en getInfoProfesor: ", e)

        return info


    """
        @brief Método que va a registrar en la tabla asistencia como que el alumno del que se pasa el dni está asistiendo a la clase que se pasa
        @author Alexinio
        @date 07/05/2020
        @param fecha, fecha en la que se está intentando registrar
        @param asignatura, asignatura a la que se está intentando registrar
        @param dni_alumno, dni del alumno que se está intentando registrar
        @param profesor, dni del profesor que imparte esa asignatura, a esa hora, en esa clase
    """
    def registrarAsistenciaDeAlumno(self,fecha, asignatura, dni_alumno, profesor):
        print("Vamos a meter info en la databse")
        try:
            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "INSERT INTO asistencia VALUES('{}', '1', '{}', '{}', '{}');".format(fecha, asignatura, dni_alumno, profesor)
            print("Query (registrarAsistenciaDeAlumno): ", query)

            self.cursor.execute(query)
            self.conexion.commit()

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion (registrarAsistenciaDeAlumno): ", e)


    """
        @brief Método que va a obtener el horario de una clase de la que se pasa su id
        @author Alexinio
        @date 07/05/2020
        @param id_clase, id de la clase de la que intenta obtener el horario
    """
    def obtenerHorarioDeUnaClase(self, id_clase):

        try:

            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "SELECT * FROM horario WHERE id_clase_fisica='{}' ORDER BY dia;".format(id_clase)
            print("Query (obtenerHorarioDeUnaClase): ", query)

            self.cursor.execute(query)
            cosa = self.cursor.fetchall()

            info = ""

            diaa = None

            for dia in cosa:
                print("DIA", dia)

                if diaa != dia[1]:
                    info = info + str(dia[1]) + "#"


                if dia[2] is not 6:
                    info = info + str(dia[3]) + "."
                else:
                    info = info + str(dia[3]) + "#"

                diaa = dia[1]


            print("Info que hemos conseguido: ", info)
            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()

            print("Excepcion en obtenerHorarioDeUnaClase: ", e)

        return info

    """
        @brief Método que va a logear a un usuario en su base de datos
        @author Alexinio
        @date 07/05/2020
        @param dni_al, dni del alumno que logear
    """
    def logearAlumno(self, dni_al):
        print("Vamos a coencctar al usuario: ", dni_al)
        try:
            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "UPDATE estudiante SET logeado='1' WHERE dni_estudiante='{}';".format(dni_al)
            print("Query (logearAlumno): ", query)

            self.cursor.execute(query)

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion (logearAlumno): ", e)

    """
        @brief Método que va a deslogear a un usuario en su base de datos
        @author Alexinio
        @date 07/05/2020
        @param dni_al, dni del alumno que deslogear
    """
    def deslogearAlumno(self, dni_al):
        print("Vamos a coencctar al usuario: ", dni_al)
        try:
            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "UPDATE estudiante SET logeado='0' WHERE dni_estudiante='{}';".format(dni_al)
            print("Query (deslogearAlumno): ", query)

            self.cursor.execute(query)

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion (deslogearAlumno): ", e)

    """
        @brief Método que va a logear a un usuario en su base de datos
        @author Alexinio
        @date 07/05/2020
        @param dni_al, dni del alumno que logear
    """
    def logearProfesor(self, dni_al):
        print("Vamos a coencctar al profesor: ", dni_al)
        try:
            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "UPDATE profesor SET logeado='1' WHERE dni_prof='{}';".format(dni_al)
            print("Query (logearProfesor): ", query)

            self.cursor.execute(query)

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion (logearProfesor): ", e)

    """
        @brief Método que va a deslogear a un usuario en su base de datos
        @author Alexinio
        @date 07/05/2020
        @param dni_al, dni del alumno que deslogear
    """
    def deslogearProfesor(self, dni_al):
        print("Vamos a coencctar al profesor: ", dni_al)
        try:
            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "UPDATE profesor SET logeado='0' WHERE dni_prof='{}';".format(dni_al)
            print("Query (deslogearProfesor): ", query)

            self.cursor.execute(query)

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion (deslogearProfesor): ", e)

    """
        @brief Método que va a comprobar si un alumno ya está logeado
        @author Alexinio
        @date 07/05/2020
        @param dni_al, dni del alumno que comprobar
    """
    def comprbarSiAlumnoYaLogeado(self, dni):
        try:

            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "SELECT * FROM estudiante WHERE dni_estudiante='{}';".format(dni)
            print("Query (comprbarSiAlumnoYaLogeado): ", query)

            self.cursor.execute(query)
            cosa = self.cursor.fetchall()

            logeado = True

            for alumno in cosa:
                print("Alumno: ", alumno)
                if alumno[4] == 0:
                    logeado = False

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion en comprbarSiAlumnoYaLogeado: ", e)

        return logeado

    """
        @brief Método que va a comprobar si un profesor ya está logeado
        @author Alexinio
        @date 07/05/2020
        @param dni_al, dni del profesor que comprobar
    """
    def comprbarSiProfesorYaLogeado(self, dni):
        try:

            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "SELECT * FROM profesor WHERE dni_profesor='{}';".format(dni)
            print("Query (comprbarSiProfesorYaLogeado): ", query)

            self.cursor.execute(query)
            cosa = self.cursor.fetchall()

            logeado = True

            for profesor in cosa:
                print("Profesor: ", profesor)
                if profesor[4] == 0:
                    logeado = False

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion en comprbarSiProfesorYaLogeado: ", e)

        return logeado


    def obtenerProfesorQueImparteAsig(self, id_asig):
        try:

            self.crearConexion()
            self.cursor = self.conexion.cursor()
            query = "SELECT * FROM asignatura WHERE id_asignatura='{}';".format(id_asig)
            print("Query (obtenerProfesorQueImparteAsig): ", query)

            self.cursor.execute(query)
            cosa = self.cursor.fetchall()

            dni_prof = None
            for asig in cosa:
                print("asig: ", asig)
                dni_prof = asig[3]

            self.cerrarConexion()

        except Exception as e:
            self.cerrarConexion()
            print("Excepcion en obtenerProfesorQueImparteAsig: ", e)

        return dni_prof
