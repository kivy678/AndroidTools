<style>
	body {
		font-family: 나눔바른고딕;
		font-size  : 1.2em;	
	}
	span {
		font-family: Hack;
	}
</style>

# <span>apk Debugger mode converter</span>

---

<span>
## 설치
1. c:> virutalenv .env --python=python3
2. c:> .env\\Script\\activate.bat
3. (.env) c:> pip3 install -r requirements.txt


## 분석 명령어
strace -s 65535 -fF -t -i -x -o /data/local/tmp/dump.txt -p [pid]
-fF 는 자식 프로세스 추적

</span>
