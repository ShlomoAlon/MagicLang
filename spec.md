# Loss‑less Lexer & Minimal AST Specification

## 1 · Lexing

### 1.1 Separators

`S = { space, tab, newline, '(', ')', '|', '"', '\' }`

### 1.2 Algorithm (loss‑less, minimal)

1. Read the next character `c`.
2. **If** `c ∈ S`
   - emit `c` as a **single‑character token**.
3. **Else**
   - accumulate consecutive **non‑separator** characters into a buffer,
   - emit the buffer as **one** token.
4. Repeat until end of input.

### 1.3 Result

The lexer returns an **ordered list of unmodified substrings**:

| Source fragment | Token produced          |
| --------------- | ----------------------- |
| separator char  | the 1‑character string  |
| run of ¬`S`     | the full multi‑char run |

No further classification is stored; only positions matter.

### 1.4 Reference Implementations

#### “Magic” version

```magic
list " " "\t" "\n" "(" ")" "|" "\"" "\\"
save SEPARATORS

func lex
  input is str
  out is list[str] do
    save tokens (list)
    
    save token ""
    for i in input do
      if SEPARATORS | contains i then
        if token then tokens | add token end_if
        tokens | add i
        
        save token ""
      else
        modify token (+ i)
      end_if
    end_for
    if token then tokens | add token end_if
    tokens
  end_do
end_func
```

#### Python counterpart

```python
SEPARATORS = set(" \t\n()|\"'")

def lex(src: str) -> list[str]:
    tokens, token = [], ""
    for ch in src:
        if ch in SEPARATORS:
            if token:
                tokens.append(token)
                token = ""
            tokens.append(ch)
        else:
            token += ch
    if token:
        tokens.append(token)
    return tokens
```

---

## 2 · AST Model (parser output)

| Node type    | Contains                                   |
| ------------ | ------------------------------------------ |
| **pipelist** | ordered list of **linelist** nodes         |
| **linelist** | ordered list of **value** nodes            |
| **value**    | a **primitive** *or* a nested **pipelist** |

`primitive ∈ { symbol, int, float, bool }`  (strings are *not* primitives).

---

## 3 · Tree Notations (for documentation only)

| Concept  | **Keyword** (prefix) notation | **Layout** notation                     |
| -------- | ----------------------------- | --------------------------------------- |
| linelist | `linelist a b c`              | `a b c` — single line                   |
| pipelist | `pipelist (linelist …) …`     | `( …\n…\n… )` — one *linelist* per line |

Reading notation **B** yields exactly the same AST as writing notation **A** literally.

### Examples

```magic
# linelist of `true false 1`
read "true false 1"
assert_eq linelist true false 1
end_assert

# pipelist with the above linelist
read "(true false 1)"
assert_eq pipelist (linelist true false 1)
end_assert

# pipelist of three identical linelists
read "(true false 1\ntrue false 1\ntrue false 1)"
assert_eq pipelist (linelist true false 1) (linelist true false 1) (linelist true false 1)
end_assert
```

---

## 4 · Formal Shape (EBNF *of the AST*, not the concrete text)

```
pipelist  ::= linelist { linelist }
linelist  ::= value    { value    }
value     ::= primitive | pipelist
primitive ::= symbol | int | float | bool
```

Concrete source code is **first** tokenised by the lexer (§1) and **then** parsed into the tree above. The two notations (§3) exist solely for human‑readable diagrams and debugging; both forms are valid *magic* code that reconstruct the same AST when fed to `read`.

---

---

## 5 · Python Example: constructing the AST objects

the following snippet shows how to build the expected tree and assert that both textual representations map to it.

```python
# --- textual inputs -------------------------------------------------
reprA = "pipelist (linelist true false 1)"  
reprB = "(true false 1)"

# --- expected python AST ---------------------------------------------------
expected = PipeList([LineList([True, False, 1])])

# --- parser calls ---------------------------------------------------
parsed_from_A = eval(read(reprA))  # means run magic on text of Repr A
parsed_from_B = read(reprB) # just read Repr B         

assert parsed_from_A == expected
assert parsed_from_B == expected

# --- slightly larger example ---------------------------------------
reprB_many = "(true false 1
true false 1
true false 1)"
expected_many = PipeList([
    LineList([True, False, 1]),
    LineList([True, False, 1]),
    LineList([True, False, 1]),
])
assert read(reprB_many) == expected_many
```

The snippet constructs `PipeList`/`LineList` instances *directly* and shows that both notations defined in §3 round‑trip to the same in‑memory objects.

## 6 · Reader behaviour

The Python `Tokens` class implements the lexer from §1. `Tokens.tokenize`
emits every separator as its own token and flushes the final accumulated
token at end of input.

The reader module builds the AST described in §2. `parse(text)` returns a
`PipeListType` for the complete program and is implemented using three helper
functions:

- **`parse_block`** – creates a pipelist until one of the supplied end tokens
  is seen.
- **`parse_line`** – collects a linelist until a newline or pipe.
- **`parse_atom`** – parses primitives or recursively parses nested blocks.

Serialising an AST via `Types.value_string` and feeding the result back to
`parse` yields an identical object. The tests assert this round‑trip property
on simple examples as well as the `examples/euler1.magic` program.

---

*End of specification*

