/*
 * Header bla
 */
import QtQuick 1.1
import QtQuick.Controls 1.4 as QtQuick1

/**
 * Parent item.
 */
Item {

    /**
     * A child with an ID.
     */
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

    /**
     * Another child with an ID. The childItem is not picked up, but the comment
     * block is added on to the previous one.
     */
    Item {
      id: childItem2
    }
}
