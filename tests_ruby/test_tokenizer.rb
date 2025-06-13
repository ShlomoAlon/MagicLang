require 'minitest/autorun'
require_relative '../tokenizer'

class TestTokenizer < Minitest::Test
  def test_basic
    text = "hello | world \n (print)"
    tokens = Tokens.tokenize(text)
    expected = ['hello', ' ', '|', ' ', 'world', ' ', "\n", ' ', '(', 'print', ')']
    assert_equal expected, tokens.tokens
  end

  def test_nontrivial
    text = (
      "seq 1 10\n" +
      "filter (eq 5)\n" +
      "get 0\n" +
      "save five\n\n" +
      "for (i) (seq 0 five) (\n" +
      "echo i\n\n" +
      "i | + 2 | echo\n" +
      ")"
    )
    tokens = Tokens.tokenize(text)
    expected = [
      'seq', ' ', '1', ' ', '10', "\n", 'filter', ' ', '(', 'eq', ' ', '5', ')', "\n",
      'get', ' ', '0', "\n", 'save', ' ', 'five', "\n", "\n", 'for', ' ', '(', 'i', ')',
      ' ', '(', 'seq', ' ', '0', ' ', 'five', ')', ' ', '(', "\n", 'echo', ' ', 'i',
      "\n", "\n", 'i', ' ', '|', ' ', '+', ' ', '2', ' ', '|', ' ', 'echo', "\n", ')'
    ]
    assert_equal expected, tokens.tokens
  end

  def test_fibonacci_program
    text = (
      "function fib (n) (\n" +
      "if (< n 2) (1)\n" +
      "else (\n" +
      "fib (n - 1) |\n" +
      "fib (n - 2) |\n" +
      "+ )\n" +
      ")\n"
    )
    tokens = Tokens.tokenize(text)
    expected = [
      'function', ' ', 'fib', ' ', '(', 'n', ')', ' ', '(', "\n", 'if', ' ',
      '(', '<', ' ', 'n', ' ', '2', ')', ' ', '(', '1', ')', "\n", 'else', ' ',
      '(', "\n", 'fib', ' ', '(', 'n', ' ', '-', ' ', '1', ')', ' ', '|', "\n",
      'fib', ' ', '(', 'n', ' ', '-', ' ', '2', ')', ' ', '|', "\n", '+', ' ',
      ')', "\n", ')', "\n"
    ]
    assert_equal expected, tokens.tokens
  end

  def test_peek_and_next
    tokens = Tokens.tokenize('a b')
    assert_equal 'a', tokens.peek
    assert_equal 'a', tokens.next
    assert_equal ' ', tokens.peek
    assert_equal ' ', tokens.next
    assert_equal 'b', tokens.peek
    assert_equal 'b', tokens.next
    assert_nil tokens.peek
    assert_nil tokens.next
    assert_nil tokens.next
  end

  def test_to_s
    tokens = Tokens.tokenize('x y')
    tokens.next
    assert_equal [' ', 'y'], eval(tokens.to_s)
  end
end
