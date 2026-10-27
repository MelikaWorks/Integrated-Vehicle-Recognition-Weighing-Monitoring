"""Selected OCR decoding method from backend_v6_3_multi_plate.py.
Model loading, vocabulary and recognition pipeline intentionally omitted.
This is a documentation excerpt, not an executable backend.
"""

def decode_prediction(pred):
    pred = pred.permute(1, 0, 2)
    pred_labels = torch.argmax(pred, dim=2)
    results = []
    for seq in pred_labels:
        prev = -1
        text = ''
        for p in seq:
            p = p.item()
            if p != blank_index and p != prev:
                text += rev_indexes.get(p, '')
            prev = p
        results.append(text)
    return results
