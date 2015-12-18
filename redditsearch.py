### Program that uses reddit API to search for keyword(s) in given subreddits ###

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import praw
from PyQt4 import QtGui, QtCore

subList = []

class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 900, 650)
		self.setWindowTitle("Your Personal Subreddit Search")
		self.setWindowIcon(QtGui.QIcon('res/reddit.png'))
		self.home()

	def home(self):
		# first label that marks the keyword bar
		keywordlbl = QtGui.QLabel(self)
		keywordlbl.setText("Enter a keyword: ")
		keywordlbl.move(10, 15)
		keywordlbl.adjustSize()

		# label next to the bars to enter subreddits
		instruclbl = QtGui.QLabel(self)
		instruclbl.setText("Enter subreddits to search: ")
		instruclbl.move(10, 45)
		instruclbl.adjustSize()

		# sets up the labels and search bars for the 10 subreddits
		for i in range(1, 11):
			global subList
			lbl = QtGui.QLabel(self)
			lbl.setText("Subreddit " + str(i) + ":")
			lbl.move(10, 70 + (30 * i))
			lbl.adjustSize()

			bar = QtGui.QLineEdit(self)
			bar.resize(bar.sizeHint())
			bar.move(90, 65 + (30 * i))
			subList.append(bar)

		# top search bar for keyword
		self.searchbar = QtGui.QLineEdit(self)
		self.searchbar.resize(self.searchbar.sizeHint())
		self.searchbar.move(keywordlbl.frameGeometry().width() + 15, 10)
		self.searchbar.returnPressed.connect(self.search)

		# search button
		searchbtn = QtGui.QPushButton("Search", self)
		searchbtn.clicked.connect(self.search)
		searchbtn.resize(searchbtn.sizeHint())
		searchbtn.move(self.searchbar.frameGeometry().width() + keywordlbl.frameGeometry().width() + 20 , 5)

		# refresh button which just searches again
		refreshbtn = QtGui.QPushButton("Refresh", self)
		refreshbtn.clicked.connect(self.search)
		refreshbtn.resize(refreshbtn.sizeHint())
		refreshbtn.move(self.searchbar.frameGeometry().width() + keywordlbl.frameGeometry().width() + searchbtn.frameGeometry().width() + 10, 5)

		# clear button to clear all subreddits entered
		clearbtn = QtGui.QPushButton("Clear", self)
		clearbtn.clicked.connect(self.clear)
		clearbtn.resize(subList[9].frameGeometry().width(), subList[9].frameGeometry().height())
		clearbtn.move(subList[9].x(), subList[9].y() + 30)

		# text browser on the right side of the screen to display results
		self.display = QtGui.QTextBrowser(self)
		self.display.setGeometry(450, 0, self.frameGeometry().width() / 2, self.frameGeometry().height())
		self.display.setOpenExternalLinks(True)
		self.show()

	# checks the new tab in the given subreddit for first 50 titles matching the given keyword
	def search_subreddit(self, prawObj, subreddit, text):
		try:
			submissions = prawObj.get_subreddit(subreddit).get_new(limit=50)
			submissionList = []
			for title in submissions:
				titleStr = str(title)
				titleStr = titleStr.split(' :: ')[1] # cleans up the title from the given submission
				url = title.permalink
				tupleObj = (titleStr, url)
				submissionList.append(tupleObj)
			submissionList = [elem for elem in submissionList if text.lower() in elem[0].lower()]
			self.display.append("<b>Related titles in r/" + subreddit + " new: </b>")
			for data in submissionList:
				self.display.append("")
				self.display.append("<a href=\"" + data[1] + "\">" + data[0] + "</a>") # hyperlink to the comments
			self.display.append("")
		except praw.errors.InvalidSubreddit:
			self.display.append("<b>" + subreddit + " does not exist.")
			self.display.append("")
		except praw.errors.NotFound:
			self.display.setText("<b>Too many requests now. Closing...</b>")
			time.sleep(3)
			exit()

	# function called to search, takes text in searchbar and uses it as keyword
	def search(self):
		text = str(self.searchbar.text())
		if (text == ''):
			self.display.setText("<b>No name entered...</b>")
		else:
			self.setWindowTitle("Your Personal Subreddit Search - " + text)
			prawObj = praw.Reddit(user_agent='search_application')
			self.display.clear()
			for subs in subList:
				trimmedSub = str(subs.text()).strip()
				if (trimmedSub != ''):
					self.search_subreddit(prawObj, trimmedSub, text)	
					
	def clear(self):
		for subs in subList:
			subs.clear()

def main():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

if __name__ == "__main__":
    main()
