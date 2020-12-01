class Card() :
    def __init__(self, suit, number) :
        self.suit = suit;
        self.number = number;
        
    def __str__(self) :
        face = self.number;
        if self.number == 1 :
            face = 'Ace';
        elif self.number == 11 :
            face = 'Jack';
        elif self.number == 12 :
            face = 'Queen';
        elif self.number == 13 :
            face = 'King';
        return f'{face} of {self.suit}';
        
    def __repr__(self) :
        return Card.__str__(self);
    
    def get_value(self) : 
        value = self.number;
        if self.number >= 11 and self.number <= 13 :
            value = 10;
        return value;
        
    def __eq__(self, other) :
        return self.number == other.number;

    def img_url(self):
        face = self.number;
        if self.number == 1 :
            face = 'ace';
        elif self.number == 11 :
            face = 'jack';
        elif self.number == 12 :
            face = 'queen';
        elif self.number == 13 :
            face = 'king';
        return str(face) + "_" + self.suit + ".png"