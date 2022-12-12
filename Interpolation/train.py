import torch
import nn

DB_PATH='SOLEDGE.db'

model =nn.retrain(db_path=DB_PATH)

#Ensure model can be pickled and unpickled.
torch.save(model,"data.pt")

