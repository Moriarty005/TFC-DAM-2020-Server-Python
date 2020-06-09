import socket
import threading
from Cosas.database_model import database_model


class ServerThread(threading.Thread):
    padre = None
    ip_bd = None
    socket = None
    protocolo = None
    database = None

    dni_usuario = None

    def __init__(self, server_padre, db_ip, socket_para_trabajar, protocol):

        print("Creamos una hebra cliente")

        threading.Thread.__init__(self)
        self.padre = server_padre
        self.ip_db = db_ip
        self.socket = socket_para_trabajar
        self.protocolo = protocol
        self.database = database_model(self.protocolo)

    def run(self):

        print("Empezamos a recibir al info")

        try:

            inputline = self.socket.recv(1024)

            while inputline != b'':



                print("Lo que recibimosen crudo: {}".format(inputline))

                inputline = str(inputline)
                inputline = inputline[2:]
                inputline = inputline[:len(inputline) - 1]

                print("Lo que recibimos: {}".format(inputline))

                if self.protocolo.comprobarEtiquetaInicio(inputline):
                    print("Entramos en el if de que el comienzo está correcto")

                    if self.protocolo.comprobarDeDondeVienenLasPeticiones(inputline) is "APP":

                        dni = self.protocolo.obtenerDniAlumnoDeProtocolo(inputline)
                        passwd = self.protocolo.obtenerPasswdAlumnoDeProtocolo(inputline)

                        self.dni_usuario = dni

                        if self.database.comprobarLogin(dni, passwd) == "profesor":
                            print("Entramos en el if que nos dice que el profesor sí está registrado")
                            if self.database.comprbarSiProfesorYaLogeado(dni) is False:
                                print("El profesor no está logeado")
                                self.database.logearProfesor(dni)

                                info_usuario = self.database.getInfoProfesor(dni, passwd)

                                #print("Vamos a hacer split de lo que nos traemos del metodode separar las cosas y to eso")

                                cosas = info_usuario.split("%")

                                print("DEBUG: Una vez vamos a enviar la info los que nos traemos de la base de datos: ", cosas)

                                self.socket.send(bytes(str("ASSISTANCESUPPORT#SERVER#LOGIN#LOGINCORRECT#TEACHER#{}#{}#{}".format(cosas[0], cosas[1], cosas[2])) + "\r\n", 'UTF-8'))

                                print("Hemos enviado el mensaje")

                            else:
                                print("El profesor YA ESTÁ LOGEADO")
                                self.socket.send(bytes(str("ASSISTANCESUPPORT#SERVER#LOGIN#LOGINERROR" + "\r\n", 'UTF-8')))

                        elif self.database.comprobarLogin(dni, passwd) == "alumno":
                            print("Entramos en el if que nos dice que el alumno sí está registrado")

                            if self.database.comprbarSiAlumnoYaLogeado(dni) is False:
                                print("El alumno no está logeado")
                                self.database.logearAlumno(dni)

                                info_usuario = self.database.getInfoAlumno(dni, passwd)

                                print("Vamos a hacer split de lo que nos traemos del metodode separar las cosas y to eso")

                                cosas = info_usuario.split("%")

                                print("DEBUG: Una vez vamos a enviar la info los que nos traemos de la base de datos: ", cosas)

                                self.socket.send(bytes(str("ASSISTANCESUPPORT#SERVER#LOGIN#LOGINCORRECT#STUDENT#{}#{}#{}".format(cosas[0], cosas[1], cosas[2])) + "\r\n", 'UTF-8'))
                            else:
                                print("El alumno YA ESTÁ LOGEADO")
                                self.socket.send(bytes(str("ASSISTANCESUPPORT#SERVER#LOGIN#LOGINERROR" + "\r\n", 'UTF-8')))
                        else:
                            self.socket.send(bytes(str("ASSISTANCESUPPORT#SERVER#LOGIN#LOGINERROR"  + "\r\n", 'UTF-8')))


                    if self.protocolo.comprobarDeDondeVienenLasPeticiones(inputline) is "RPI4":
                        print("El mensaje que nos llega es de la rpi4: ", inputline)

                        if self.protocolo.checkWhatActionDoFromTheRaspberry(inputline) == "REGISTERASSISTANCE":
                            print("Vamos a registrar asistencia del alumno ya que nos lo ha dicho la raspberry pi")

                            dni_al = self.protocolo.getStudentDniFromTheRaspberry(inputline)
                            asig = self.protocolo.getSubjectFromTheRaspberry(inputline)
                            fecha = self.protocolo.getRegisterDateFromTheRaspberry(inputline)
                            prof = self.database.obtenerProfesorQueImparteAsig(asig)
                            self.database.registrarAsistenciaDeAlumno(fecha, asig, dni_al, prof)

                            print("Ya hemos insertado la info en la base de datos")
                        elif self.protocolo.checkWhatActionDoFromTheRaspberry(inputline) == "GETTIMETABLE":

                            print("La raspberry  quiere obtener los datos de los horarios")

                            clase = self.protocolo.getClaseParaObtenerHorarios(inputline)

                            info = self.database.obtenerHorarioDeUnaClase(clase)

                            self.socket.send(bytes(str("ASSISTANCESUPPORT#SERVER#GETTIMETABLE#{}".format(info)) + "\r\n", 'UTF-8'))



                inputline = self.socket.recv(1024)

                    # cosa = self.protocolo.comprobarEtiquetaInicio(inputline)
                    # print("Cosa:", cosa)

        except Exception as e:
            print("Excepcion en la hebra de servidor: ", e)
            if(self.dni_usuario != None):
                self.database.deslogearProfesor(self.dni_usuario)
                self.database.deslogearAlumno(self.dni_usuario)

            self.socket.close()
            exit()

        finally:
            if (self.dni_usuario != None):
                self.database.deslogearProfesor(self.dni_usuario)
                self.database.deslogearAlumno(self.dni_usuario)
            self.socket.close()
            exit()
