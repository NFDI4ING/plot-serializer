from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Proxy(Generic[T]):
    """
    Base class for any class that wants to surface the same functionality as an
    object stored within it. The object from which the functionality is replicated
    is called "delegate". This way we can add or change functionality to an object
    from a library we don't control or modify without changing the behavior of
    programs using this object.

    Example:
    .. highlight:: python
    .. code-block:: python

        # Presume we have the following counter class from a package we can't
        # modify ourselves:

        class Counter:
            def __init__(self) -> None:
                self._counter = 0

            def increment(self) -> None:
                self._counter += 1

            def current_count(self) -> int:
                return self._counter

        # We can create a Counter that looks like it starts at a negative value
        # by doing the following

        class NegativeCounter(Proxy[Counter]):
            def current_count(self) -> int:
                # Call the original method and subtract 10
                return self.delegate.current_count() - 10

        # Create a negative counter by providing the underlying object
        negative_counter = NegativeCounter(Counter())

        # We can still call methods from the original counter
        negative_counter.increment()

        # And yet, we also get our changed functionality
        assert negative_counter.current_count() == -9

    Args:
        Generic (_type_): Type of the delegate object
    """

    def __init__(self, delegate: T) -> None:
        """
        Initializes this proxy.

        Args:
            delegate (T): Object to delegate calls to
        """
        self._delegate = delegate

    def __getattr__(self, __name: str) -> Any:
        # If we haven't found the method/field locally, get it from the delegate instead
        return getattr(self._delegate, __name)

    @property
    def delegate(self) -> T:
        """
        Property that allows access to the delegate object which was given in the
        constructor. This is useful when wanting to perform actions or access state
        from the underlying object.

        Returns:
            T: The delegate object
        """
        return self._delegate
