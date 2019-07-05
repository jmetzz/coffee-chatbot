


## How to use it

If you don't have enough data, you can generate using chatette (for NLU) and 
story augmentation for the dialogue.
 
```bash
$ core genarate
```

Generates both NLU and dialogue data.
If you want you can generate them separately: 

```bash
$ core chatette
$ core augment
```

Before you are able to test the chatbot, you need to train the models (NLU & Dialogue)

```bash
$ core train
```

The training procedure generates the model that you can use to test the chatbot. 
You will find the model ni the `models` directory.

```bash

```
