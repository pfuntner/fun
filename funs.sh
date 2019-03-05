foo() {
  echo "foo sees: $*"
}

function bar() {
  echo "bar sees: $*"
}

echo "main sees: $*"
foo
bar
