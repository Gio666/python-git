# -*- coding: UTF-8 -*-
import os

""" Clase Cliente que representa cada uno de los clientes y su respectiva informacion"""
class Cliente:
	def __init__(self, cedula, pin, nombre, saldo, etc):
		self.cedula = cedula
		self.pin = pin
		self.nombre = nombre
		self.saldo = saldo
		self.etc = etc
		
""" Clase Cajero que tiene el monto actual en el cajero y las denominaciones de billetes que posee"""
class CajeroAutomatico:
	def __init__(self, cincuentaMil, veinteMil, diezMil, cincoMil, dosMil, mil):
		self.cincuentaMil = cincuentaMil
		self.veinteMil = veinteMil
		self.diezMil = diezMil
		self.cincoMil = cincoMil
		self.dosMil = dosMil
		self.mil = mil
		
	def getMontoTotal(cajero):
		return 50000 * cajero.cincuentaMil + 20000 * cajero.veinteMil + 10000 * cajero.diezMil + 5000 * cajero.cincoMil + 2000 * cajero.dosMil + 1000 * cajero.mil
		
	def dispensarDinero(self, cliente, monto):
	
		copiaMonto = monto
		
		cincuentaMil = 0
		veinteMil = 0
		diezMil = 0
		cincoMil = 0
		dosMil = 0
		mil = 0
		
		while monto >= 50000:
			cincuentaMil += 1
			monto -= 50000
		while monto >= 20000:
			veinteMil += 1
			monto -= 20000
		while monto >= 10000:
			diezMil += 1
			monto -= 10000
		while monto >= 5000:
			cincoMil += 1
			monto -= 5000
		while monto >= 2000:
			dosMil += 1
			monto -= 2000
		while monto >= 1000:
			mil += 1
			monto -= 1000
		
		self.cincuentaMil -= cincuentaMil
		self.veinteMil -= veinteMil
		self.diezMil -= diezMil
		self.cincoMil -= cincoMil
		self.dosMil -= dosMil
		self.mil -= mil
		
		cliente.saldo -= copiaMonto
		
		desgloceDeBilletes = "Se dispensaron " + str(copiaMonto) + " usando los siguientes billetes:\n"		
		desgloceDeBilletes += (str(cincuentaMil) + " de 50 mil\n" if cincuentaMil > 0 else "")
		desgloceDeBilletes += (str(veinteMil) + " de 20 mil\n" if veinteMil > 0 else "")
		desgloceDeBilletes += (str(diezMil) + " de 10 mil\n" if diezMil > 0 else "")
		desgloceDeBilletes += (str(cincoMil) + " de 5 mil\n" if cincoMil > 0 else "")
		desgloceDeBilletes += (str(dosMil) + " de 2 mil\n" if dosMil > 0 else "")
		desgloceDeBilletes += (str(mil) + " de mil\n" if mil > 0 else "")
		
		mostrarEstadoDelCajero(cajero)
		print desgloceDeBilletes
		
	def realizarDeposito(self, cliente, monto):
	
		copiaMonto = monto
		
		cincuentaMil = 0
		veinteMil = 0
		diezMil = 0
		cincoMil = 0
		dosMil = 0
		mil = 0
		
		while monto >= 50000:
			cincuentaMil += 1
			monto -= 50000
		while monto >= 20000:
			veinteMil += 1
			monto -= 20000
		while monto >= 10000:
			diezMil += 1
			monto -= 10000
		while monto >= 5000:
			cincoMil += 1
			monto -= 5000
		while monto >= 2000:
			dosMil += 1
			monto -= 2000
		while monto >= 1000:
			mil += 1
			monto -= 1000
		
		self.cincuentaMil += cincuentaMil
		self.veinteMil += veinteMil
		self.diezMil += diezMil
		self.cincoMil += cincoMil
		self.dosMil += dosMil
		self.mil += mil
		
		cliente.saldo += copiaMonto
		
		desgloceDeBilletes = "Se depositaron " + str(copiaMonto) + " a su cuenta, se depositaron:\n"		
		desgloceDeBilletes += (str(cincuentaMil) + " de 50 mil\n" if cincuentaMil > 0 else "")
		desgloceDeBilletes += (str(veinteMil) + " de 20 mil\n" if veinteMil > 0 else "")
		desgloceDeBilletes += (str(diezMil) + " de 10 mil\n" if diezMil > 0 else "")
		desgloceDeBilletes += (str(cincoMil) + " de 5 mil\n" if cincoMil > 0 else "")
		desgloceDeBilletes += (str(dosMil) + " de 2 mil\n" if dosMil > 0 else "")
		desgloceDeBilletes += (str(mil) + " de mil\n" if mil > 0 else "")
		
		mostrarEstadoDelCajero(cajero)
		print desgloceDeBilletes
		
	def transferirFondos(self, cliente, beneficiario, monto):
		if (cliente.saldo >= monto):
			cliente.saldo -= monto
			beneficiario.saldo += monto
		
"""Esta funcion crea clientes ficticios para que el cajero pueda funcionar"""
def crearClientes(listaDeClientes):
	listaDeClientes.append(Cliente(1, 2222, "Pedro Perez", 25000, "Buen cliente"))
	listaDeClientes.append(Cliente(22, 1234, "Andrea Trejos", 153500, "Ojos azules"))
	listaDeClientes.append(Cliente(123, 0000, "Diana Porras", 3000, "Vive en Cartago"))
	
"""Busca un cliente por su cedula en la listaDeClientes y lo retorna de existir"""
def buscarCliente(cedula, listaDeClientes):
	for cliente in listaDeClientes:
			if cliente.cedula == cedula:
				return cliente 

"""Imprime la lista de clientes"""				
def imprimirListaDeClientes(listaDeClientes):
	for cliente in listaDeClientes:
		print cliente.nombre

"""Despliega en pantalla el saldo del cliente"""
def consultarSaldo(cliente):
	mostrarEstadoDelCajero(cajero)
	
"""Realiza la accion necesaria para retirar efectivo del cajero"""
def retirarEfectivo(cliente, cajero):
	mostrarEstadoDelCajero(cajero)
	monto = input("De sus " + str(cliente.saldo) + " colones, cuanto desea retirar?\nDigite el monto en multiplos de mil colones ")
	if (monto % 1000 == 0): #Si el monto fue digitado en multiplos de mil
		if (cliente.saldo >= monto): #Si el cliente tiene los fondos requeridos
			cajero.dispensarDinero(cliente, monto)
		else:
			mostrarEstadoDelCajero(cajero)
			print "Fondos insuficientes, su cuenta tiene " + str(cliente.saldo) + " colones e intento retirar " + str(monto) + " colones."
	else:
		mostrarEstadoDelCajero(cajero)
		print "El monto debio de ser digitado en multiplos de mil colones, " + str(monto) + " no es un monto valido."

"""Realiza la accion necesaria para depositar efectivo del cajero"""
def depositarEfectivo(cliente, cajero):
	mostrarEstadoDelCajero(cajero)
	monto = input("Digite el monto que desea depositar en multiplos de mil colones ")
	if (monto % 1000 == 0): #Si el monto fue digitado en multiplos de mil
			cajero.realizarDeposito(cliente, monto) #Deposite la plata
	else:
		mostrarEstadoDelCajero(cajero)
		print "El monto debio de ser digitado en multiplos de mil colones, " + str(monto) + " no es un monto valido."
		
"""Realiza la accion necesaria para transferir fondos entre cuentas"""
def transferirEfectivo(cliente):
	mostrarEstadoDelCajero(cajero)
	monto = input("Digite el monto a tranferir ")
	if (cliente.saldo >= monto):
		cedulaBeneficiario = input("Digite el número de cedula de la persona que recibira los fondos: ")
		beneficiario = buscarCliente(cedulaBeneficiario, listaDeClientes)
		if (beneficiario != None):
				cajero.transferirFondos(cliente, beneficiario, monto)
				print str(monto) + " transferidos exitosmente a la cuenta de " + beneficiario.nombre
		else:
			print "El numero de cedula" + str(cedula) + "no corresponde a ninguno de nuestros clientes"
	else:
		mostrarEstadoDelCajero(cajero)
		print "Fondos insuficientes, su cuenta tiene " + str(cliente.saldo) + " colones e intento transferir " + str(monto) + " colones."
		
"""Limpia la pantalla"""
def limpiarPantalla():
	os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
	
"""Muestra el estado actual del cajero automatico"""
def mostrarEstadoDelCajero(cajero):
	limpiarPantalla()
	print "El cajero tiene " + str(CajeroAutomatico.getMontoTotal(cajero)) + " colones."
	print str(cajero.cincuentaMil) + " de 50k | " + str(cajero.veinteMil) + " de 20k | " + str(cajero.diezMil) + " de 10k | " + str(cajero.cincoMil) + " de 5k | " + str(cajero.dosMil) + " de 2k | " + str(cajero.mil) + " de 1k"
	print ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
	print "::::::::::::::::::::::::: Cajero Automático :::::::::::::::::::::::::"
	print ":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"
	
def menuDeCliente(cliente):
	print cliente.nombre + ", en su cuenta hay " + str(cliente.saldo) + " colones, que desea hacer?"
	print "1. Consultar Saldo"
	print "2. Retirar efectivo"
	print "3. Depositar"
	print "4. Transferir"
	print "5. Salir"

"""\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"""
"""Aqui termina la declaracion de funciones e inicia el codigo a ejecutar del cajero."""
"""//////////////////////////////////////////////////////////////////////////////////"""

cajero = CajeroAutomatico(10,20,30,40,50,100) #Se crea un cajero con billetes de todas las denominaciones
listaDeClientes = [] #Se crea una lista de clientes
crearClientes(listaDeClientes) #Se crean clientes ficticios

mostrarEstadoDelCajero(cajero)
print "1. Ingresar Tarjeta"
print "2. Salir"
opcionDeUsuario = input("Que desea hacer? digite 1 o 2: ")

while(opcionDeUsuario == 1):

	mostrarEstadoDelCajero(cajero)
	cedula = input("Digite su número de cedula: ")
	cliente = buscarCliente(cedula, listaDeClientes)
	
	if (cliente != None):#Si el cliente existe
	
		mostrarEstadoDelCajero(cajero)
		pin = input("Hola " + cliente.nombre + ", digite su pin para continuar: ")
		
		if (pin == cliente.pin):
		
			mostrarEstadoDelCajero(cajero)
			
			opcion = 1
			while (opcion != 5):
				menuDeCliente(cliente)
				opcion = input("Que desea hacer? digite 1, 2 , 3, 4 o 5 ")
			
				if opcion == 1:
					mostrarEstadoDelCajero(cajero)
					consultarSaldo(cliente) 
				elif opcion == 2:
					retirarEfectivo(cliente, cajero)
				elif opcion == 3:
					depositarEfectivo(cliente, cajero)
				elif opcion == 4:
					transferirEfectivo(cliente)
				elif opcion == 5:
					mostrarEstadoDelCajero(cajero)
				else:
					mostrarEstadoDelCajero(cajero)
					print "Opcion Invalida"
		else:
			mostrarEstadoDelCajero(cajero)
			print "pin invalido."
	else:
		mostrarEstadoDelCajero(cajero)
		print "El numero de cedula " + str(cedula) + " no corresponde a ninguno de nuestros clientes."

	print "1. Ingresar Tarjeta"
	print "2. Salir"
	opcionDeUsuario = input("Que desea hacer? digite 1 o 2: ")
			