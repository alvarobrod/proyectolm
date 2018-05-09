def formathora(hora):
	dia = hora.split('-')[2]
	mes = hora.split('-')[1]
	año = hora.split('-')[0]
	return '{}/{}/{}'.format(dia, mes, año)