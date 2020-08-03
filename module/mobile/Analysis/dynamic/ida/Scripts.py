R0 = lambda: GetRegValue('R0')
R1 = lambda: GetRegValue('R1')
R2 = lambda: GetRegValue('R2')
R3 = lambda: GetRegValue('R3')
R4 = lambda: GetRegValue('R4')
R5 = lambda: GetRegValue('R5')
R6 = lambda: GetRegValue('R6')
R7 = lambda: GetRegValue('R7')
R8 = lambda: GetRegValue('R8')
R9 = lambda: GetRegValue('R9')
R10 = lambda: GetRegValue('R10')
R11 = lambda: GetRegValue('R11')
R12 = lambda: GetRegValue('R12')
RSP = lambda: GetRegValue('SP')
RLR = lambda: GetRegValue('LR')
RPC = lambda: GetRegValue('PC')

def InlineMem(m, l):
	return ' '.join(map(lambda x: x.encode('hex').upper(), GetManyBytes(m, l)))

def FetchMem(m, l):
	data = map(ord, GetManyBytes(m, l))
	
	lData = len(data)
	
	out = ""
	
	for offset in xrange(0, lData, 16):
		out += "%08X :" % (offset, )
		for dx in xrange(offset, min(offset+16, lData)):
			out += ' %02X' % (data[dx], )
		out += "\n"
	
	return out
	
def PrintHex(x):
	return '0x%08X' % (x)
	
def distance(a,b):
	return PrintHex(max(a,b) - min(a,b))
	
def MemToFile(fp, ptr, size):
	with open(fp, 'wb') as fd:
		fd.write(GetManyBytes(ptr, size))
		fd.flush()

	
def jiagu_init_bp():
	dp = GetRegValue('PC') - 0x681C
	print '0x%08X' % dp
	
	def __Break(x, comment=None):
		AddBpt(dp + x)
		if not comment is None:
			MakeComm(dp + x, comment)
			
	__Break(0x60D0, 'Call MMAP')
	__Break(0x83D8, 'Watch LR')
	__Break(0x187C, 'dlsym')
	__Break(0x6B14, 'Next Addr')
	__Break(0x29F8, 'str batch')
	__Break(0x2FE8, 'uncomp lib mmap')
	
	

	