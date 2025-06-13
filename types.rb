class LineList < Array
  def to_magic
    map do |v|
      if v.is_a?(PipeList)
        "(#{v.to_magic})"
      else
        v.to_magic
      end
    end.join(' ')
  end
end

class PipeList < Array
  def to_magic
    map { |v| v.to_magic }.join("\n")
  end
end

class String
  def to_magic
    self
  end
end

class Integer
  def to_magic
    to_s
  end
end

class Float
  def to_magic
    to_s
  end
end

class Symbol
  def to_magic
    to_s
  end
end

class TrueClass
  def to_magic
    to_s
  end
end

class FalseClass
  def to_magic
    to_s
  end
end

module Types
  def self.value_string(obj)
    obj.to_magic
  end
end
