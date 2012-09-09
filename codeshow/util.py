def truncate(path, length=30):
	segments = path.split('/')
	s = segments.pop()
	while len(segments) > 0 and len(s) + len(segments[-1]) <= (length-4):
		s = segments.pop() + '/' + s
	if len(segments) > 0:
		s = '.../' + s
	return s

def is_binary(filename):
    with open(filename, 'rb') as f:
        CHUNKSIZE = 1024
        while True:
            chunk = f.read(CHUNKSIZE)
            if '\0' in chunk: return True
            if len(chunk) < CHUNKSIZE: break
    return False
