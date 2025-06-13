class LineList < Array
  def to_magic(nested = 0)
    self.map { |v| v.respond_to?(:to_magic) ? v.to_magic(nested + 1) : v.to_s }.join(' ')
  end
end

class PipeList < Array
  def to_magic(nested = 0)
    parts = self.map { |v| v.respond_to?(:to_magic) ? v.to_magic(nested) : v.to_s }
    inner = parts.join("\n")
    nested.zero? ? inner : "(#{inner})"
  end
end

class String
  def to_magic(_nested = 0)
    self
  end
end

class Integer
  def to_magic(_nested = 0)
    to_s
  end
end

class Float
  def to_magic(_nested = 0)
    to_s
  end
end

class Symbol
  def to_magic(_nested = 0)
    to_s
  end
end

class TrueClass
  def to_magic(_nested = 0)
    to_s
  end
end

class FalseClass
  def to_magic(_nested = 0)
    to_s
  end
end

module Types
  def self.value_string(obj)
    if obj.respond_to?(:to_magic)
      obj.to_magic
    else
      obj.to_s
    end
  end
end
