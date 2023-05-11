class Loc:
   def  __init__(self, path, row, col):
    self.file_path = path
    self.row = row
    self.col = col

   def display(self):
      return print(self.file_path,':', self.row, ':',self.col)
   

   def get_data(self):
      return self.file_path + ':'+ str(self.row+1) + ':' + str(self.col+1)