from components.units import *
from constants import X_SCALE, Y_SCALE

TILE_TEMPLATES = {(15, 7):
["""                 
                   
       \      ,      
  .                    
                         
             *             
id0                          
    -                      
                  /      
       |               
                     
           .       
                 """,
"""                 
                   
                     
                       
        l0,---､          
        s0⎛     ⎞          
id0      r0⎝     ⎠           
         i0‛---’           
       n0a        
       n0b      
                     
                   
                 """,
"""                 
  l0,---､          
  s0⎛     ⎞          
   r0⎝     ⎠           
     i0‛---’             
      n0a           
id0     n0b           
             l1,---､       
           s1⎛     ⎞     
          r1⎝     ⎠    
          i1‛---’    
       n1a  
     n1b  """,
"""                 
         l1,---､   
         s1⎛     ⎞   
          r1⎝     ⎠    
   l0,---､  i1‛---’      
   s0⎛     ⎞  n1a   
id0 r0⎝     ⎠   n1b   
    i0‛---’    l2,---､     
  n0a s2⎛     ⎞   
  n0br2⎝     ⎠  
            i2‛---’  
       n2a  
     n2b  """]}
NO_TILE = """                 
                   
                     
                       
                         
                           
                             
                           
                         
                       
                     
                   
                 """



UNITS = {Carrier: "<ΞΞ#",
         Cruiser: "-=≡=",
         Destroyer: "K",
         Dreadnought: "<Ξ=◊",
         Fighter: "#",
         Flagship: "◇<⟨⟩=",
         WarSun: "(%)",
         PDS: "#-",
         SpaceDock: "(Y)",
         Infantry: "⏻",
         Mech: "Ξ"}

BLANK_UNITS = {k: ' ' * len(v) for k, v in UNITS.items()}

PLANET_TEMPLATE = """L0,---､
S0⎛     ⎞s0
R0⎝     ⎠r0
I0‛---’i0
"""

WORMHOLE_TEMPLATE = """.-.
( w )
 ‛-’"""