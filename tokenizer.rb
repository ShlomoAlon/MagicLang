class Tokens
  attr_reader :tokens

  def initialize(tokens)
    @tokens = tokens
    @cur = 0
  end

  def self.tokenize(text)
    separators = ['(', ')', "\n", ' ', '|', '"']
    result = []
    builder = ''
    text.each_char do |ch|
      if separators.include?(ch)
        unless builder.empty?
          result << builder
          builder = ''
        end
        result << ch
      else
        builder << ch
      end
    end
    result << builder unless builder.empty?
    new(result)
  end

  def peek
    return nil if @cur >= @tokens.length
    @tokens[@cur]
  end

  def next
    tok = peek
    @cur += 1 if tok
    tok
  end

  def to_s
    @tokens[@cur..-1].inspect
  end
end
