class Enum : public QtQuick.Item {
public:
/// Enum type
/// in multiple lines
enum class Direction {
Up, ///< Go up
/// Go down
Down
};
enum class IsThisOk { ///< Inline comment
/** Comma after last entry */
CommaAfterLast
};
};
