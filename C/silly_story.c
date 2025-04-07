/**
 * Silly Story in C
 * @author Charles Li
 * @version 1.0.0
 * @date Mar 26 2025
 * Given a large piece of text - say, Shakespear's Midsummer Night's Dream,
 * produce a new text that is written in the same style.
 */

 #include <stdio.h>
 #include <stdlib.h>
 #include <string.h>
 #include <time.h>
 
 #define MAX_ARGS 3
 #define MAX_WORD_LEN 50
 #define MAX_CONTEXT 100
 #define HASH_SIZE 10007
 
 // Structure to store a list of words that follow a given context
 typedef struct WordList {
     char **words;
     int size;
     int capacity;
 } WordList;
 
 // Structure to store a context and its corresponding word list
 typedef struct ContextMap {
     char **context;
     int context_len;
     WordList wordList;
     struct ContextMap *next;
 } ContextMap;
 
 // Hash table to store context mappings
 ContextMap *hashTable[HASH_SIZE];
 int context_len;
 int num_words;
 
 // DJB2 Hash function to generate a unique key for a given context
 unsigned long hash(const char *const *context) {
     unsigned long h = 5381;
     for (int i = 0; i < context_len; i++) {
         for (const char *c = context[i]; *c; c++) {
             h = ((h << 5) + h) + *c;
         }
     }
     return h % HASH_SIZE;
 }
 
 // Find an existing context in the hash table or create a new one
 ContextMap *find_or_create_context(char **context) {
     unsigned long h = hash((const char *const *)context);
     ContextMap *entry = hashTable[h];
     while (entry) {
         int match = 1;
         for (int i = 0; i < context_len && match; i++) {
             if (strcmp(entry->context[i], context[i])) {
                 match = 0;
             }
         }
         if (match) return entry; // Found existing context
         entry = entry->next;
     }
     // Create a new context entry
     entry = malloc(sizeof(ContextMap));
     entry->context = malloc(context_len * sizeof(char *));
     for (int i = 0; i < context_len; i++) {
         entry->context[i] = strdup(context[i]);
     }
     entry->context_len = context_len;
     entry->wordList.words = NULL;
     entry->wordList.size = 0;
     entry->wordList.capacity = 0;
     entry->next = hashTable[h];
     hashTable[h] = entry;
     return entry;
 }
 
 // Add a word to the word list of a given context
 void add_word_to_context(ContextMap *context, const char *word) {
     if (context->wordList.size == context->wordList.capacity) {
         context->wordList.capacity = context->wordList.capacity ? context->wordList.capacity * 2 : 4;
         context->wordList.words = realloc(context->wordList.words, context->wordList.capacity * sizeof(char *));
     }
     context->wordList.words[context->wordList.size] = strdup(word);
     context->wordList.size++;
 }
 
 // Function to count the total number of unique words in the hash table
 int count_unique_words() {
     char **uniqueWords = malloc(MAX_WORD_LEN * sizeof(char *));
     int uniqueCount = 0;
 
     // Iterate through the hash table and count unique words
     for (int i = 0; i < HASH_SIZE; i++) {
         ContextMap *entry = hashTable[i];
         while (entry) {
             for (int j = 0; j < entry->wordList.size; j++) {
                 const char *word = entry->wordList.words[j];
 
                 // Check if this word is already in the uniqueWords array
                 int found = 0;
                 for (int k = 0; k < uniqueCount && !found; k++) {
                     if (!strcmp(uniqueWords[k], word)) {
                         found = 1;
                     }
                 }
 
                 // If the word is not found, add it to uniqueWords
                 if (!found) {
                     uniqueWords[uniqueCount] = strdup(word);
                     uniqueCount++;
                 }
             }
             entry = entry->next;
         }
     }
 
     // Clean up allocated memory
     for (int i = 0; i < uniqueCount; i++) {
         free(uniqueWords[i]);
     }
     free(uniqueWords);
 
     return uniqueCount;
 }
 
 // Read the input file and build the context-word associations
 void associate(FILE *reader) {
     char **context = malloc(context_len * sizeof(char *));
     for (int i = 0; i < context_len; i++) {
         context[i] = strdup(""); // Initialize context with empty strings
     }
     char word[MAX_WORD_LEN];
     while (fscanf(reader, "%49s", word) == 1) {
         ContextMap *contextEntry = find_or_create_context(context);
         add_word_to_context(contextEntry, word);
         free(context[0]);
         for (int i = 0; i < context_len - 1; i++) {
             context[i] = context[i + 1];
         }
         context[context_len - 1] = strdup(word);
     }
     for (int i = 0; i < context_len; i++) {
         free(context[i]);
     }
     free(context);
 }
 
// Generate and print a new text using the learned word associations
void generate_words() {
    srand(time(NULL));
    
    // If context_len is 0, generate words randomly from the unique words in the text
    if (context_len == 0) {
        int word_count = 0;
        
        // Traverse hash table to collect all unique words
        while (word_count < num_words) {
            // Pick a random context entry
            int rand_index = rand() % HASH_SIZE;
            ContextMap *contextEntry = hashTable[rand_index];
            
            while (contextEntry) {
                // Pick a random word from this context's word list
                const char *word = contextEntry->wordList.words[rand() % contextEntry->wordList.size];
                printf("%s%s", word, strcmp(word, "\n") == 0 ? "" : " ");
                word_count++;
                contextEntry = contextEntry->next;
            }
        }
        printf("\n");
        return;
    }

    // Regular case when context_len > 0
    char **context = malloc(context_len * sizeof(char *));
    for (int i = 0; i < context_len; i++) {
        context[i] = strdup(""); // Initialize context with empty strings
    }

    int word_count = 0;
    int words_found = 1;

    // Start generating words
    while (word_count < num_words && words_found) {
        // Find the context in the hash table
        ContextMap *contextEntry = find_or_create_context(context);
        
        // If no words found in this context, stop generation
        if (contextEntry->wordList.size == 0) {
            words_found = 0;
        } else {
            // Pick a random word from the context's word list
            const char *word = contextEntry->wordList.words[rand() % contextEntry->wordList.size];
            printf("%s%s", word, strcmp(word, "\n") == 0 ? "" : " ");
            
            // Update context for next word
            free(context[0]);
            for (int j = 0; j < context_len - 1; j++) {
                context[j] = context[j + 1];
            }
            context[context_len - 1] = strdup(word);
            word_count++;
        }
    }
    
    // Print final newline
    printf("\n");

    // Free memory for context
    for (int i = 0; i < context_len; i++) {
        free(context[i]);
    }
    free(context);
}

 // Main function to handle command-line arguments and run the program
 int main(int argc, char *argv[]) {
     if (argc < MAX_ARGS) {
         fprintf(stderr, "Usage: %s <text_file> <context_length>\n", argv[0]);
         return 1;
     }
     
     context_len = atoi(argv[2]);
 
     FILE *file = fopen(argv[1], "r");
     if (!file) {
         perror("Error opening file");
         return 1;
     }
     associate(file); // Build context-word associations
     fclose(file);
     
     num_words = count_unique_words() - context_len;
     if (num_words < 0) {
        fprintf(stderr, "%s needs at least %d words", argv[1], context_len);
        return 1;
     }

     generate_words();

     return 0;
 }
 