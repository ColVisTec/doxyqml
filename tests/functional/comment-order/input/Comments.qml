import QtQuick 1.1

/// @brief %Comments test case
Item {
    /// @brief Property foo
    property int foo

    /// @name My group
    /// @{

    /// @brief Property myFoo, part of my group
    property int myFoo

    /// @brief Property myBar, part of my group
    property int myBar

    /// @}

    /// @brief Assignment to parent class property
    visible: true

    /** @name Their group
     * @{
     */

    /** @brief Property theirFoo, part of their group */
    property int theirFoo

    /** @brief Property theirBar, part of their group */
    property int theirBar

    /** @} */

    /// @brief Property baz
    property int baz
}
