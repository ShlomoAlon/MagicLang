require_relative 'tokenizer'
require_relative 'types'

# Parse *magic* source code into a PipeList AST.
# Equivalent to the Python reader implementation.

def parse(text)
  tokens = Tokens.tokenize(text)
  parsePipe(tokens)
end

# Parse a sequence of lines until one of the end tokens is encountered.

def parsePipe(tokens, ends = [])
  ast = PipeList.new
  while (tok = tokens.peek) && !ends.include?(tok)
    ast << parseLine(tokens, ends)
  end
  ast
end

# Parse a single line, stopping at a newline or pipe token.

def parseLine(tokens, ends = [])
  new_lines = ['|', "\n"]

  return LineList.new unless tokens.peek

  if new_lines.include?(tokens.peek)
    tokens.next
    return LineList.new
  end

  ast = LineList.new

  while (tok = tokens.peek) && !new_lines.include?(tok) && !ends.include?(tok)
    atom = parseAtom(tokens)
    ast << atom unless atom.nil?
  end

  tokens.next if tokens.peek && new_lines.include?(tokens.peek)

  ast
end

# Parse the next primitive or nested block from the token stream.

def parseAtom(tokens)
  return nil unless tokens.peek

  token = tokens.peek

  case token
  when '('
    tokens.next
    result = parsePipe(tokens, [')'])
    raise SyntaxError, 'Unclosed parenthesis' unless tokens.peek == ')'
    tokens.next
    result
  when ' '
    tokens.next
    nil
  when 'true'
    tokens.next
    true
  when 'false'
    tokens.next
    false
  else
    tok = tokens.next
    if tok.match?(/^-?\d+$/)
      tok.to_i
    elsif tok.match?(/^-?\d+\.\d+$/)
      tok.to_f
    else
      tok
    end
  end
end
