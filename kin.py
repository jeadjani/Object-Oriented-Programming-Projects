from argparse import ArgumentParser
from json import load
from relationships import relationships 
from sys import argv



class Person():
    """A class that represents a person in a family
    
    Attributes: 
        name: string of a person's name
        gender: string of a person's gender
        parents: list of instance of a persons parents
        spouse: instance of a person's spouse
    """
    def __init__(self,name,gender):
        """ Initializes the Person object with name and gender, sets parents and spouse to an empty list.
        
        Args: takes name and gender to create person object
        
        Attributes:
            name: String attribute that establishes a person's name.
            spouse: String attribute that indicates a person's spouse.
            parents: A list containing string attributes of the name of someones parents.
        
        Returns:
            returns dictionary; cdict
        
        Side effects:
            Sets the name and gender of a person.
            Initializes list of parents as an attribute of each instance of the Person class.
            Sets the value of spouse to "None"
        """
        self.name=name
        self.gender=gender
        self.parents=[]
        self.spouse=None
    
        
    def add_parent(self,parents):
        """
        Args:
            parents: instance of a Person
        """
        self.parents.append(parents)
        
    def set_spouse(self,spouse):
        """
        Args: 
            instance of a Person
        Attributes:
            spouse: instance of a Person object that is the spouse of the person
        """
        self.spouse = spouse
        
    def connections(self):
        """
        Args:
            None
        Returns:
            returns cdict
        """
        cdict={self:""}
        queue=[self]
        while queue is True:
            p=queue.pop(0)
            personpath=cdict[p]
            for parent in p.parents:
                if parent not in cdict:
                    connection1 = personpath+"P"
                    cdict[parent]=connection1
                    queue.append(parent)
            if 'S' not in personpath and p.spouse != None and p.spouse not in cdict:
                connection2=personpath +"S"
                cdict[p.spouse] = connection2
                queue.append(p.spouse)
        return cdict
            
                    
          
    def relation_to(self, person):
        """
        Args:
            an instance of Person other person
        Returns:
             returns collection if it is empty
             returns relationship path of person or distant relative 
        """
        link1=self.connections()
        link2=person.connections()
        collection=[]
        for relative in set(link1) & set(link2):
            collection.append(f"{link1[relative]}:{link2[relative]}")
        
        if collection == []:
            return None
        path=min(collection, key=len)
        if path in relationships:
            return relationships[path][self.gender]
        else:
            return "distant relative"
      
        
        
class Family():
    """ Class with the individuals of a family. Uses the instances from the Person object to define 
    relationships of parents and spouses.
    
    Attributes:
        people: dictionary of persons with key defined by person. 
    
    """
    def __init__(self,individuals):
        """Method that intializes the insance of the Family class.
        
        Attributes:
            people: Group of individuals to be placed in a dictionary self.people.
        Args:
            individuals: Dictionary of a person's name and gender
                parents: Dictionary of a persons parents, with a list of the person's parents' name.
                couples: List of lists, inner list with two names indicating individuals that are couples. 
        Returns:
                none
        Side Effects:
                none
        """
        self.people = {}
        for person, gender in individuals["individuals"].items():
            self.people[person]=Person(person, gender)
        for person, parents in individuals["parents"].items():
            name = self.people[person]
            for parent_person in parents:
                parent = self.people[parent_person]
                name.add_parent(parent)
        
        for couple in individuals["couples"]:
            individual1=self.people[couple[0]]
            individual2=self.people[couple[1]]
            individual1.set_spouse(individual2)
            individual2.set_spouse(individual1)
               
                         
    def relation(self, name1, name2):
       """ Method that gives the relation of the first and second person
       Args:
            name1 and name2, the keys used for self.people to be stored in variables that can be used 
            in the relation_to method
       Returns:
            None or a kinship term expressed as a string.
       Side Effects:
            none
       """
    
      
       individual1=self.people[name1]
       individual2=self.people[name2]
       return individual1.relation_to(individual2)
        
        
    
def main(filepath, name1, name2):
    """Function that uses the JSON file to read and load contents in order to define relationship between the first and second person
    Args:
        filepath: path to file, JSON
        name1: The name of the first person in the file.
        name2: The name of the second person in the file.
    Side Effects:
         If the names given aren't related a message that says; "{name1} is not related to {name2}" will be shown.
         If the names are related a message saying; "{name1} is {name2}'s {relatedness}" will be printed. 
    """
    with open(filepath, "r", encoding="utf-8") as f:
        individuals = load(f)
        fam=Family(individuals)
        relatedness = fam.relation(name1,name2)
        if relatedness is None:
            print (f"{name1} is not related to {name2}")
        else:
            print (f"{name1} is {name2}'s {relatedness}")
   
    
def parse_args(args):
    """Function that takes a list of command-line arguments to create an instance of ArgumentParser class
    and usr add_argument to define one command line object per parameter of main(), then pass the list of 
    command-line arguments the function received to return the namespace object. 
    Args:
        command-line arguments: list made by add_argument
    Returns:
        The namespace object created by parse_args.
    """
    parser = ArgumentParser()
    parser.add_argument("filepath", help="Path to file with family data")
    parser.add_argument("name1", help="Name of first person")
    parser.add_argument("name2", help="Name of second person")
    return parser.parse_args(args)

if __name__ =="__main__":
    title=parse_args(argv[1:])
    main(title.filepath, title.name1, title.name2)