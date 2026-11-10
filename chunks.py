from chunks1 import fix_size_chunk
def read_in_chunks(file_object, chunk_size = 1024):
    context = []
    position = 0
    while True:
        chunk_1 = file_object.read(chunk_size)
        if not chunk_1:
            break
        a = chunk_1.rfind(" ")
        b = chunk_1.rfind("\n")
        valid = [x for x in (a,b) if x >= 0]
        boundary = max(valid) if valid else -1

        if boundary == -1:
            chunk_1 = chunk_1 + file_object.read(chunk_size)
            boundary = chunk_1.rfind(" ")
            if boundary == -1:
                yield " ".join(context) + " " + chunk_1
                break
        chunk_2 = chunk_1[:boundary + 1]#(return 0 to boundry)
        position += len(chunk_2)
        file_object.seek(position)
        result = " ".join(context)
        chunk_used = result + " " + chunk_2
        words = chunk_2.split()[-4:]
        context = words.copy()
        yield chunk_used.strip() # yield return chunk back to whosoever is iterating it  and remember where it left off

def chunk(chunk_size = 1000):
    with open('adi_profile.txt', 'r', encoding = 'utf-8') as f:
        for piece in (f, chunk_size):
            yield piece