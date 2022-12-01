"""A circular genome for simulating transposable elements."""

from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)



class Genome(ABC):
    """Representation of a circular enome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet

    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet







class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.lst = []
        self.ID = []
        for i in range(n):
            self.lst.append("-")
            self.ID.append(0)
        self.active_lst = []
        self.count = 0 

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        if pos > len(self.lst):
            pos = pos % len(self.lst)

        self.count += 1 
        if self.lst[pos] == "A":
            self.disable_te(self.ID[pos])
        
        lst1, ID1 = self.lst[0:pos], self.ID[0:pos]
        lst2, ID2 = self.lst[pos:], self.ID[pos:]
        for i in range(length):
            lst1.append("A")
            ID1.append(self.count)
        self.lst = lst1 + lst2
        self.ID = ID1 + ID2 

        self.active_lst.append(self.count)

        return self.count


    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """

        for i in range(len(self.ID)):
            if self.ID[i] == te:
                index_ID = i 
                break
        
        if self.lst[index_ID] == "x":
            return None 
    
        len_ID = 0 
        for i in range(len(self.ID)):
            if self.ID[i] == te:
                len_ID += 1 

        return self.insert_te(index_ID + offset, len_ID)




    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        for i in range(len(self.ID)):
            if self.ID[i] == te:
                self.lst[i] = "x"
        
        self.active_lst.remove(te)
        

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return self.active_lst 

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.lst)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        return "".join(self.lst)



geome = ListGenome(20)
print(geome)
geome.insert_te(40, 10)
print(geome)
#geome.insert_te(3, 10)
#print(geome)

#print(geome.active_tes())

#geome.insert_te(4, 10)
#print(geome)

#print(geome.active_tes())
#geome.copy_te(2,12)
#print(geome)
#print(geome.active_tes())


class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        self.lst = []
        self.index_next = []
        self.ID = []
        for i in range(n):
            self.lst.append("-")
            self.index_next.append((i+1) % n)
            self.ID.append(0)
        
        self.active_lst = []
        self.count = 0 

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        
        self.count += 1 

        i = 0
        count = 0 
        for _ in range(pos-1):
            i = self.index_next[i]
            count+=1
        
        if self.lst[i] == "A":
            self.disable_te(self.ID[i])
        
        old_next = self.index_next[i]
        self.index_next[i] = len(self.lst)
        for _ in range(length-1):
            self.index_next.append(len(self.index_next)+1)
        self.index_next.append(old_next)


        for i in range(length):
            self.lst.append("A")
            self.ID.append(self.count)

        self.active_lst.append(self.count)

        return self.count


    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """ 
        if te not in self.active_lst:
            return None

        i = 0
        count = 0
        while self.ID[i] != te:
            i = self.index_next[i]
            count += 1
        te_pos = count 
        count = 0
        while self.ID[i] == te:
            i = self.index_next[i]
            count += 1
        print(self.index_next)
        print(te_pos)
        return self.insert_te(len(self.index_next) + (te_pos+offset), count)


    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        for i in range(len(self.ID)):
            if self.ID[i] == te:
                self.lst[i] = "x"
        
        self.active_lst.remove(te)

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return self.active_lst

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.lst)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        self.new = []
        i = 0
        while len( self.new) != len(self.lst): 
            self.new.append(self.lst[i])
            i = self.index_next[i]
        return "".join( self.new)

#geome = LinkedListGenome(4)
#print(geome)
##geome.insert_te(1, 2)
#print(geome)
#print(geome.active_tes())
#geome.insert_te(2, 2)
#print(geome)

#geome2 = LinkedListGenome(20)
#print(geome2)
#geome2.insert_te(5, 10) 
#print(geome2)
#geome2.insert_te(10, 10)
#print(geome2)
#geome2.copy_te(2, 20)
#print(geome2)
#geome2.copy_te(2, -15)
#print(geome2)