from graphql import parse
from graphql.language.ast import Field, FragmentDefinition, FragmentSpread

def get_fields_from_query(q):
  # Count field names from the parsed document so aliases and squashed
  # whitespace cannot hide a field from the cost check.
  try:
    ast = parse(q)
  except Exception:
    return []

  fragments = {}
  for definition in ast.definitions:
    if isinstance(definition, FragmentDefinition):
      fragments[definition.name.value] = definition

  fields = []

  def walk(selection_set, depth=0):
    if selection_set is None or depth > 50:
      return

    for selection in selection_set.selections:
      if isinstance(selection, Field):
        fields.append(selection.name.value)
        walk(selection.selection_set, depth + 1)
      elif isinstance(selection, FragmentSpread):
        fragment = fragments.get(selection.name.value)
        if fragment is not None:
          walk(fragment.selection_set, depth + 1)
      else:
        walk(getattr(selection, 'selection_set', None), depth + 1)

  for definition in ast.definitions:
    walk(getattr(definition, 'selection_set', None))

  return fields

def get_depth(q):
  depth = 0
  max_depth = 0
  for c in q:
    if c == '{':
      depth += 1
      if depth > max_depth:
        max_depth = depth
    elif c == '}' and depth > 0:
      depth -= 1
  return max_depth
