# Object Classes

## How These Work

The object class modules are named with the signature of the record it describes. For example, Armor (ARMO) record objects and any associated enums will be located in ARMO.py. This should be fairly straightforward.

## Fields and Aliases

Each object class defined here is first defined with a full list of the fields/subrecords associated with that record. These fields are defined with the XEditAttribute descriptor which should encapsulate the logic for generically getting/setting any value type in these records. For each field, we will define a class attribute that is the same as the signature name. Additionally, we may define a few human-friendly aliases.

> For example, the `OBND` field will be available on the object as an `obnd` attribute, and also additionally as an `object_bounds` attribute that can be considered an alias to the `obnd` attribute. It's possible for a field to have multiple aliases (e.g. `BAMT` is available as `bash_material` and also `alternate block material`), and also possible for a field to have no aliases (e.g. `DATA` happens to be `data` and there's really no need for an alias as it would also just be called `data`.)

In general, users should expect that the lower-cased signature name attribute (e.g. `obnd`) to always exist and thus are super stable API. The aliases (like `object_bounds`) may change in the future from release to release as I understand more of what they actually do.

For the time being, the aliases come from two sources:

1. The field labels in xEdit
2. uesp.net's list of mod file format records

Frequently the two lists don't agree on what to call a record, so I tried to include both nomenclature (as aliases) whenever they both sound valid and helpful.

## Helper Methods

An object class here may also come with sensible helper methods and properties. For example, the TXST class has a helper property called `file_paths` which will automatically return you a list of values from all the file path fields on the record. What's available depends on which object class and what makes sense for the corresponding record.
