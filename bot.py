from SkypePing import SkypePing

print('Bot are running...')

sk = SkypePing(tokenFile="token", autoAck=True)
sk.loop()

