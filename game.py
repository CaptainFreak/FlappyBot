import pygame,random,math,sys,time
from pygame.locals import *
import numpy as np
#sigmoid 
def nonlin(x):
	return 1/(1+np.exp(-x))

#sorting bots with descending order of their fitness 
def top_scorer(bots,scores):
	for i in range(9):
		for j in range(9-i):
			if scores[j]<scores[j+1]:
				scores[j],scores[j+1],bots[j],bots[j+1]=scores[j+1],scores[j],bots[j+1],bots[j]
	return bots,scores			

#crossover of bots
def mating(bots):
	for i in range(9):
		bots[i].net[1],bots[i+1].net[1]=bots[i+1].net[1],bots[i].net[1]
		bots[i].net[0],bots[i+1].net[0]=bots[i+1].net[0],bots[i].net[0]
		
	return bots

#random mutation
def mutation(bots):
	for b in range(10):
		for l in range(2):
			if l:
				for n in range(7):
					if random.uniform(0,1)>0.85:
						bots[b].net[l][n]+=random.uniform(-0.5,0.5)

			else:
				for r in range(3):
					for c in range(6):
						if random.uniform(0,1)>0.85:
							bots[b].net[l][r][c]+=random.uniform(-0.5,0.5)
				
	return bots

#removing bots with less fitness
def weaklings_getting_killed(bots):
	for i in range(3):
		bots[9-i]=chromosome()
	return bots	


class chromosome:
	def __init__(self):
		self.net=[np.array([np.array([random.uniform(-1, 1) for i in range(6)]) for j in range(3)]), np.array([random.uniform(-1, 1) for k in range(7)])]
	def feed(self,input):
			hidden=nonlin(np.dot(input,self.net[0]))
			return (np.dot(hidden,self.net[1][1:])+self.net[1][0])
#game 				 
class game:
	def __init__(self):
		self.screen=pygame.display.set_mode((250,400))
		self.bg=pygame.image.load('images/back.png')
		self.bg=pygame.transform.scale(self.bg,(250,400))
		self.birds=[pygame.transform.scale(pygame.image.load('images/birdh.png').convert_alpha(),(30,30)),pygame.transform.scale(pygame.image.load('images/birdu.png').convert_alpha(),(30,30)),pygame.transform.scale(pygame.image.load('images/birdd.png').convert_alpha(),(30,30))]
		self.pipe_up=pygame.transform.scale(pygame.image.load('images/upipe.png').convert_alpha(),(40,350))
		self.pipe_down=pygame.transform.scale(pygame.image.load('images/dpipe.png').convert_alpha(),(40,350))
		self.dist=110
		self.pipex=250
		self.birdy=150
		self.jump=0
		self.gravity=5
		self.jspeed=5
		self.dead=False
		self.ico=0
		self.score=0
		self.pos=random.randint(-80,80)
		self.out=False
	def pipe(self):
		pass

	def animate_pipe(self):
		self.pipex-=1
		if self.pipex<40 and not self.out:
			self.score+=1
			self.out=True
		if(self.pipex<-25):
			self.pipex=250
			self.pos=random.randint(-100,100)
			self.out=False
			

	def animate_bird(self):
		if self.jump:
			self.jspeed-=1
			self.jump-=1
			self.birdy-=self.jspeed
		else:
			self.birdy+=self.gravity
			self.gravity+=0.2
		
		urect=pygame.Rect(self.pipex,210+self.dist-self.pos-10,self.pipe_up.get_width(),self.pipe_up.get_height())
		drect=pygame.Rect(self.pipex,0-self.dist-self.pos-10,self.pipe_down.get_width(),self.pipe_down.get_height())	
		bird=pygame.Rect(70,self.birdy,self.birds[self.ico].get_width(),self.birds[self.ico].get_height()-10)
		
		if urect.colliderect(bird) or drect.colliderect(bird):
			self.dead=True
			self.pipex=250
			self.pos=random.randint(-100,100)
			self.score=0
			self.birdy=150	
			self.gravity=5
	
		if self.birdy>405 or self.birdy<10:
			self.dead=True
			self.pipex=250
			self.pos=random.randint(-100,100)
			self.score=0
			self.birdy=150	
			self.gravity=5





	def run(self):
		clock=pygame.time.Clock()
		pygame.font.init()
		font=pygame.font.SysFont("Arial",50)
		pygame.display.set_caption("FlappyBird")
		for j in range(10):
				bots=[chromosome() for i in range(10)]
		scores=[0 for i in range(10)]		
		for i in range(1200):
			for j in range(10):	
				frames=0
				while not self.dead:
					clock.tick(5500)
					frames+=0.1
					for event in pygame.event.get():
						if event.type==pygame.QUIT:
							sys.exit()
						'''if event.type==pygame.KEYDOWN and not self.dead:
							self.jump=15	
							self.gravity=3
							self.jspeed=9'''			
							
					self.screen.fill((255,255,255))
					self.screen.blit(self.bg,(0,0))
					upy=210+self.dist-self.pos
					dpy=0-self.dist-self.pos
					self.screen.blit(self.pipe_up,(self.pipex,upy))
					self.screen.blit(self.pipe_down,(self.pipex,dpy))
					self.screen.blit(font.render(str(self.score),-1,(255,255,255)),(140,10))								
					self.screen.blit(self.birds[self.ico],(70,self.birdy))
					
					#input vector
					input=[self.birdy,self.pipex-70,upy]
					
					#output of neural network
					decision=bots[j].feed(input)
					
					#checking jump conditions
					if(decision>=0 and not self.dead):
						self.jump=15	
						self.gravity=3
						self.jspeed=9

					if self.dead:
						self.ico=2
					elif self.jump:
						self.ico=1
					self.animate_pipe()
					self.animate_bird()
					pygame.display.update()		

				scores[j]=frames
				print ('Generation={i},Chromosome={j},Fitness={s}'.format(i=i,j=j,s=scores[j]))
				self.dead=False
			bots,scores=top_scorer(bots,scores)
			bots=mating(bots)
			bots=mutation(bots)
			bots=weaklings_getting_killed(bots)


#main
if __name__=="__main__":
	game().run()