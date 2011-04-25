def levenshtein(s1,s2):
	l1 = len(s1)
	l2 = len(s2)
	
	m = [[0 for j in range(l1+1)] for i in range(l2+1)]
	m[0] = range(0, l1+1)
	for i in range (l2+1):
		m[i][0] = i
		
	for i in range(1, l2+1):
		for j in range(1, l1+1):
			if s2[i-1] == s1[j-1]:
				m[i][j] = m[i-1][j-1]
			else:
				m[i][j] = min(m[i-1][j], m[i][j-1], m[i-1][j-1])+1
	return m[l2][l1]
	