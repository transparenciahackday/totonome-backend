# create initial data
# run this to create the database records that load on the first migrate

# nomes-aceites
acceptedNames = []
acceptedNamesFile = open("nomes-aceites.txt",'r')
for line in acceptedNamesFile:
	if '"' in line:
		name = line.split('"')[1]
		acceptedNames.append(name)

# nomes-rejeitados
refusedNames = []
refusedNamesFile = open("nomes-rejeitados.txt",'r')
for line in refusedNamesFile:
	if '"' in line:
		name = line.split('"')[1]
		refusedNames.append(name)

output = open("initial_data.json","w")
output.write("[")
totalCount = 1
count = 1
for name in acceptedNames:
	output.write("{")
	output.write('"pk":'+str(totalCount)+',')
	output.write('"model": "rest.word",')
	output.write('"fields":')
	output.write("{")
	output.write('"name": "'+name+'",')
	output.write('"corrects": 0,')
	output.write('"wrongs": 0,')
	output.write('"accepted": true')
	output.write("}")
	output.write("}")
	if count < len(acceptedNames):
		output.write(",")
	count += 1
	totalCount += 1
output.write(",")

count = 1
for name in refusedNames:
	output.write("{")
	output.write('"pk":'+str(totalCount)+',')
	output.write('"model": "rest.word",')
	output.write('"fields":')
	output.write("{")
	output.write('"name": "'+name+'",')
	output.write('"corrects": 0,')
	output.write('"wrongs": 0,')
	output.write('"accepted": false')
	output.write("}")
	output.write("}")
	if count < len(refusedNames):
		output.write(",")
	count += 1
	totalCount += 1
output.write("]")

output.close()
