/*
 * Header bla
 */
import QtQuick 1.1
import QtQuick.Controls 1.4 as QtQuick1

/**
 * Parent item.
 */
Item {

    /// @page page1 A page describing the content of the QML file
    ///
    /// Some Description Here
    Item {

        id: childItem

        /** An attribute that is is ignored */
        componentAttribute: value

        /**
         * A function in a component. Even this is ignored
         * @param type:string str The string to append 'a' to.
         * @return type:string The new string.
         */
        function itemFunction(str) {
            return str + "a";
        }
    }

    /// Another block that gets added to the page which could describe why
    /// childItem2 is here
    Item {
      id: childItem2
    }
}
