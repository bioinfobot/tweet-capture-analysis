class BioBotEndPoints: 
    """ Contains a set of attributes that provides the endpoints of the 
    each destined directory 
    
    Attributes
    ----------
    self.contents   ->  website-code/Bioinfobot/content/en
    
    self.json_data	->  tweet-capture-analysis/data	
    
	self.images     -> tweet-capture-analysis/images
    
    Returns
    -------
    str 
		all attributes are return as a string
    
    """


    def __init__(self):
        ROOT_PATH = "~/"
        self.contents = "website-code/Bioinfobot/content/en/posts"
        self.json_data = "tweet-capture-analysis/data"
        self.images = "tweet-capture-analysis/images"
