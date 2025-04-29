# Magic Programming Language Principles

## 1. Homoeconomity (Homoiconic Economy)
The principle of homoeconomity states that **code and data are the same**. This means:

- Every piece of data get's printed to console as valid code to recreate itself.
- The ast is represented in data structures in magic
- The code is represented in an obvious form

## 2. Environment-Centric Symbol Resolution
Everything in Magic is parsed as a symbol first and resolved by its local environment. Different environments can interpret symbols differently. This means:

- All tokens are initially treated as symbols
- Each environment defines its own rules for symbol resolution
- The same symbol might behave differently in different environments
- Environments can provide context-specific behavior

### Example:
```magic
# In the echo environment:
hello     # Looks up 'hello' in env, if not found treats as string "hello"
\hello    # Directly treated as string "hello" (escape symbol)
$hello      # always treat as env lookup errors out if it fails
```

## 3. Pipeline Transparency
All checking, saving, and output functions pass through their input unchanged. This enables seamless pipeline composition. This means:

- Functions like print, assert, save return their input value
- Side effects don't break the pipeline flow
- Multiple checks can be chained without modifying data
- Debugging can be inserted anywhere in a pipeline

### Example:
```magic
seq 0 10
print
filter eq 0
print
sum

# Assertions in pipeline:
getValue
assert positive
transform
assert valid
save
```

## 4. Line Break Equivalence
In Magic, a newline followed by a pipe (`|`) is equivalent to a double newline. Both break the pipeline flow. This means:

- Single newline with pipe = Double newline
- Both terminate the current pipeline
- A new line starts a new pipeline context
- Pipelines must be written on a single line or use line continuation

### Example:
```magic
# These are equivalent:
seq 0 10 | print | sum

seq 0 10
print
sum

# This breaks the pipeline:
seq 0 10
| print  # New pipeline, error: no input
```

This principle enables:
- Clean visual formatting
- Consistent pipeline behavior
- Clear pipeline boundaries
- Flexible code layout

More principles will be added as the language evolves... 