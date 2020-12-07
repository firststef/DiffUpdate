# Diff update

Realizati o aplicație care sa producă un update prin diferente intre doua fișiere binare.
Aplicația primește la intrare versiunea curentă a unui fisier binar, precum si mai multe
versiune precedente ale acestuia si creaza o lista de comenzi (de tipul insert / delete /change) prin care se poate ajunge de la unul din fișierele precedente la fișierul curent. Lista în
cauză este encodata într-un fișier binar. Cu acel fișier binar, pornind de la unul dintre fișierele
cu versiune mai veche, se poate obține fișierul cel mai nou.

## INPUT
### INPUT: difupdate.py create abc.latest abc.ver1 abc.ver2 abc.ver3
(in cazul de mai sus, se presupune ca ultima versiune este 4)
Rezultatul e un fișier cu numele “abc.diff” care conține informațiile necesare ca sa se poate
ajunge de la versiunea 1 , 2 respectiv 3 la versiunea 4 (latest)

### INPUT: difupdate.py update abc.ver2 abc.diff

Rezultatul este ca se va crea un fișier abc.latest obținut aplicand operații de tipul (insert,
delete sau change bytes) pe fișierul abc.ver2. Aceste operații sunt descrise în abc.diff (ca fiind
cele necesare ca sa trecem de la versiunea 2 la versiunea 4 (latest).

OUTPUT: