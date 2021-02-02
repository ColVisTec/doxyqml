using namespace QtQuick;
class Endcond : public QtQuick.Item {
public:
/**
 * The 'foo' property
 */
Q_PROPERTY(int foo READ dummyGetter_foo_ignore)
/// @cond TEST

/// A test property, not visible by default
Q_PROPERTY(int test READ dummyGetter_test_ignore)
/// @endcond TEST
private:
/// @cond
var visible;
/// @endcond
};
