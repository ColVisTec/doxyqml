import QtQuick 1.0

/// This item conteins an inline component and a Component
Item {
    /// This is inline component example
    component ThisIsInlineComponent: Text 
    { 
        /// This is inline component property 
        property string someProperty
    }

    /// This is a component example 
    property Component thisIsAComponent: Text {
        /// This is Component property that will not be documented
        property string someProperty
    }

    /// This is a column
    Column {
        id: col
    }
}
