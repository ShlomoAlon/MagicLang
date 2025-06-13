require 'minitest/autorun'
require_relative '../types'

class TestTypes < Minitest::Test
  def test_builtin_to_magic
    assert_equal 'hello', 'hello'.to_magic
    assert_equal '42', 42.to_magic
    assert_equal '3.5', 3.5.to_magic
    assert_equal 'foo', :foo.to_magic
  end

  def test_linelist
    list = LineList.new([1, 'a', :b])
    assert_equal '1 a b', list.to_magic
  end

  def test_pipelist
    pipe = PipeList.new([
      LineList.new([:x]),
      LineList.new([:y, 2])
    ])
    assert_equal "x\ny 2", pipe.to_magic
  end

  def test_nested_pipe
    inner = PipeList.new([LineList.new([:z])])
    outer = LineList.new([:echo, inner])
    assert_equal 'echo (z)', outer.to_magic
  end

  def test_value_string_wrapper
    list = LineList.new([:a, 1])
    assert_equal 'a 1', Types.value_string(list)
  end
end
