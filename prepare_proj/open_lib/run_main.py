from smart_g2p.trans import sentranslit as trans

if "__main__" == __name__:
    trans('1999년 8월29일은 john가 mary을 만난 날로 매년 3시15분 방 3-147에서 의식이 거행된다', if_num=False, if_sym=False)
    '1999년 8월29일은 존이 메리를 만난 날로 매년 3시15분 방 3-147에서 의식이 거행된다'