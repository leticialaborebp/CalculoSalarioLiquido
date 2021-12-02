__all__ = ('calcular_passagem', 'calcular_ir', 'format_number', 'calcular_inss')

# importing functools for reduce()
import functools

def calcular_passagem(salario): 
	return salario * 6 / 100.0

def calcular_inss(salario):
  if salario <= 1100:
    desconto_inss = (0.075 * salario)
  elif salario <= 2203.49:
    desconto_inss = (82.5+((salario - 1100 * 0.09)))
  elif salario <= 3305.23:
    desconto_inss = (181.81 + ((salario - 2203.49) *0.12))
  elif salario <= 6433.57:
    desconto_inss = (314.02 + (salario -3305.23) * 0.14)
  else:
    desconto_inss = 751.99
  return round (desconto_inss, 2)
	
def calcular_ir(salario, desconto_inss):

	base_calculo_ir = salario - desconto_inss

	if base_calculo_ir < 1903.98:
		return 0

	if base_calculo_ir >= 1903.99 and base_calculo_ir < 2826.65: 
		porcentagem_desconto_ir = 7.5
		deducao_imposto = 142.80

	if base_calculo_ir >= 2826.66 and base_calculo_ir < 3751.05: 
		porcentagem_desconto_ir = 15
		deducao_imposto = 354,80

	if base_calculo_ir >= 3751.06 and base_calculo_ir < 4664.68: 
		porcentagem_desconto_ir = 22.5
		deducao_imposto = 636,13

	if base_calculo_ir >= 4664.68: 
		porcentagem_desconto_ir = 27.5
		deducao_imposto = 869.36
    
	return (base_calculo_ir * porcentagem_desconto_ir / 100.0) - deducao_imposto

def format_number(number, precision=2, group_sep='.', decimal_sep=','):
	
	assert isinstance(number, float), 'Float esperado'
	assert isinstance(precision, int), 'Int esperado'
	assert isinstance(group_sep, str), 'Str esperado'
	assert isinstance(decimal_sep, str), 'Str esperado'

	number = '%.*f' % (max(0, precision), number)
	number = number.split('.')

	integer_part = number[0]

	if integer_part[0] == '-':
	    sign = integer_part[0]
	    integer_part = integer_part[1:]
	else:
	    sign = ''

	if len(number) == 2:
	    decimal_part = decimal_sep + number[1]
	else:
	    decimal_part = decimal_sep + '00'

	integer_part = list(integer_part)
	c = len(integer_part)

	while c > 3:
	    c -= 3
	    integer_part.insert(c, group_sep)

	return sign + ''.join(integer_part) + decimal_part

def calcular_salario():
	try:
		# Entrada de dados
		salario = float(input("Qual e o seu salario bruto? "))
		passagem = input("Passagem? (S ou N) ")
		outros_descontos = float(input("Informe outros descontos fora IR e INSS (0 para nenhum): "))

		# passagem
		desconto_passagem = 0

		if passagem.lower() not in ('s', 'n'):
			raise Exception ('Informe s ou n para passagem')

		if passagem.lower() == 's':
			desconto_passagem = calcular_passagem(salario)

		# INSS
		desconto_inss = calcular_inss(salario)

		# IR
		desconto_ir = calcular_ir(salario, desconto_inss)
    
    # Totais finais
		total_liquido_mes = functools.reduce((lambda x,y: x-y), [salario, desconto_passagem, desconto_inss, desconto_ir, outros_descontos])
		total_ganho_ano = total_liquido_mes * 12

		total_imposto_mes = functools.reduce((lambda x,y: x+y), [desconto_inss, desconto_ir])
		total_imposto_ano = total_imposto_mes * 12

		try:
			print (("Valor bruto informado: R$ %s") % format_number(salario))
			print (("Salario liquido/mes: R$ %s") % format_number(total_liquido_mes))
			print (("Total imposto/mes: R$ %s") % format_number(total_imposto_mes))
			print (("Total imposto/ano: R$ %s") % format_number(total_imposto_ano))
			print (("Total desconto passagem: R$ %s") % format_number(desconto_passagem))
			print (("Outros descontos: R$ %s") % format_number(outros_descontos))
			print (("Total ganho/ano liquido R$ %s") % format_number(total_ganho_ano))
		except Exception as e:
			print(e)

	except Exception as e:
		print(e)

if __name__ == '__main__':
	calcular_salario()