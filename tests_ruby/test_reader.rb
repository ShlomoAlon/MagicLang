require 'minitest/autorun'
require_relative '../parse'
require_relative '../types'

class TestReader < Minitest::Test
  def roundtrip(src)
    ast = parse(src)
    assert_equal ast, parse(Types.value_string(ast))
  end

  def test_roundtrip_simple
    ['1 2 | 3', 'eq 0 | or (item | mod 3 | eq 0)'].each do |src|
      roundtrip(src)
    end
  end

  def test_roundtrip_example_file
    src = File.read('examples/euler1.magic')
    roundtrip(src)
  end

  def test_empty_line_roundtrip
    src = "1\n\n2"
    ast = parse(src)
    assert_equal 3, ast.length
    assert ast[1].is_a?(Array) && ast[1].empty?
    assert_equal ast, parse(Types.value_string(ast))
  end

  def test_roundtrip_nontrivial_program
    src = (
      "seq 1 10\n" +
      "filter (eq 5)\n" +
      "get 0\n" +
      "save five\n\n" +
      "for (i) (seq 0 five) (\n" +
      "echo i\n\n" +
      "i | + 2 | echo\n" +
      ")"
    )
    roundtrip(src)
  end
end
