from pororo import Pororo


### MAIN ###
if "__main__" == __name__:
    print("[run_pororo][__main__]")
    g2p = Pororo(task="g2p", lang="kr")
    print(g2p("1999년 8월29일은 john가 mary을 만난 날로 매년 3시15분 방 3-147에서 의식이 거행된다"))