using namespace QtQuick;
/// @brief %Comments test case
class Comments : public QtQuick.Item {
public:
/// @brief Property foo
Q_PROPERTY(int foo READ dummyGetter_foo_ignore)
/// @name My group
/// @{

/// @brief Property myFoo, part of my group
Q_PROPERTY(int myFoo READ dummyGetter_myFoo_ignore)
/// @brief Property myBar, part of my group
Q_PROPERTY(int myBar READ dummyGetter_myBar_ignore)
/// @}
private:
/// @brief Assignment to parent class property
var visible;
/** @name Their group
 * @{
 */
public:
/** @brief Property theirFoo, part of their group */
Q_PROPERTY(int theirFoo READ dummyGetter_theirFoo_ignore)
/** @brief Property theirBar, part of their group */
Q_PROPERTY(int theirBar READ dummyGetter_theirBar_ignore)
/** @} */
/// @brief Property baz
Q_PROPERTY(int baz READ dummyGetter_baz_ignore)
};
